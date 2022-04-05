import cv2

class Inference_gauge(object):
    def __init__(self, needle_ratio=None, gauge_ratio = None):
        """
        @param boxN: [[gauge0_xywh(tuple), gauge1_xywh, ...], [needle0_xywh, needle1_xywh, ...]]
        @param needle_ratio: [needle0_ratio, needle1_ratio, needle2_ratio...]
        @param gauge_ratio: [gauge0_ratio, gauge1_ratio, ...]
        """
        if needle_ratio is None:
            needle_ratio = 0.35
        if gauge_ratio is None:
            gauge_ratio = [0, 0.325, 0.45, 0.575, 0.7, 1] #[3, 5, 10, 20]
        self.needle_ratio = needle_ratio
        self.gauge_ratio = gauge_ratio


    def needle_point_pixel(self, position):
        Nx1, Ny1, Nx2, Ny2 = position
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

    def result(self, position):
        pixel_result = self.needle_point_pixel(position)
        height, width, c = self.gauge_shape
        needle_pos_ratio = pixel_result / height
        return self.map_needle_to_gauge(needle_pos_ratio)

if __name__ == "__main__":
    # boxN: [[gauge0_xywh(tuple), gauge1_xywh, ...], [needle0_xywh, needle1_xywh, ...]]
    # boxN: [[gauge0_xywh(tuple), gauge1_xywh, ...], [needle0_xywh, needle1_xywh, ...]]
    position = [[125.5078125, 41.45494079589844, 480.3267517089844, 1080.0, 0.0],
                [1452.1253662109375, 43.88685607910156, 1782.43115234375, 1080.0, 0.0],
                [839.5030517578125, 25.795944213867188, 1090.293212890625, 1080.0, 0.0]]
    image_resolution = (1920, 1080)

    image = "108.jpg"
    inference = Inference_gauge(None, None)
    print(inference.result(position))