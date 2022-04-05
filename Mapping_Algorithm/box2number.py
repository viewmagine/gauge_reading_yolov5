import cv2

class Inference_gauge(object):
    def __init__(self, position, needle_ratio=None, gauge_ratio = None):
        """
        @param boxN: [[gauge0_xywh(tuple), gauge1_xywh, ...], [needle0_xywh, needle1_xywh, ...]]
        @param needle_ratio: [needle0_ratio, needle1_ratio, needle2_ratio...]
        @param gauge_ratio: [gauge0_ratio, gauge1_ratio, ...]
        """
        self.boxN = position
        if needle_ratio is None:
            needle_ratio = 0.35
        if gauge_ratio is None:
            gauge_ratio = [0, 0.325, 0.45, 0.575, 0.7, 1] #[3, 5, 10, 20]
        self.needle_ratio = needle_ratio
        self.gauge_ratio = gauge_ratio


    def needle_point_pixel(self):
        Nx1, Ny1, Nx2, Ny2 = self.boxN
        print("Needle Point", Nx1, Ny1, Nx2, Ny2)
        return (1 - self.needle_ratio) * Ny1 + self.needle_ratio * Ny2

    def map_needle_to_gauge(self, needle_relative_pos):
        for i in range(len(self.gauge_ratio)-1):
            if needle_relative_pos >self.gauge_ratio[i]:
                if needle_relative_pos < self.gauge_ratio[i+1]:
                    print(needle_relative_pos, self.gauge_ratio[i], self.gauge_ratio[i+1])
                    return [0, 3, 5, 10, 20, 999][i:i+2]
        print(needle_relative_pos, self.gauge_ratio[0])
        return -1

    def result(self):
        pixel_result = self.needle_point_pixel()
        height, width, c = self.gauge_shape
        needle_pos_ratio = pixel_result / height
        return self.map_needle_to_gauge(needle_pos_ratio)

if __name__ == "__main__":
    # boxN: [[gauge0_xywh(tuple), gauge1_xywh, ...], [needle0_xywh, needle1_xywh, ...]]
    position = [[(130, 0, 230, 1075), (865, 0, 190, 1080), (1487, 0, 329, 1079)], [(250, 650, 80, 128 ),(925, 591, 80, 174), (1573, 604, 90, 165)]]
    image_resolution = (1920, 1080)

    image = "108.jpg"
    inference = Inference_gauge(position, None, None)
    print(inference.result())