# convert image to LCD version
import cv2
from pathlib import Path
from glob import glob

def process_img(path: Path):
    print('processing', path)
    img_path = path.absolute()
    img = cv2.imread(str(img_path))
    img = cv2.flip(img, 1)
    print(img.shape)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGR565)
    rows,cols,_ = img.shape
    output_path = Path(img_path.parent.parent.joinpath('./rgb565/output').with_stem(img_path.stem).with_suffix('.raw')).absolute()
    print("output to", output_path)
    with open(output_path, 'wb') as fp:
        img_data = []
        for i in range(rows):
            line = []
            for j in range(cols):
                x, y = img[i, j]
                pixel = int(x<<8|y).to_bytes(2, 'big')
                line.append(pixel)
            img_data.append(b"".join(line))
        fp.write(b"".join(img_data))

    # cv2.waitKey(0) # waits until a key is pressed
    # cv2.destroyAllWindows() # destroys the window showing image


if __name__ == "__main__":
    for input_img in glob("./resources/rgb888/*.png"):
        input_img_path = Path(input_img).absolute()
        process_img(input_img_path)
