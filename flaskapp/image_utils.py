from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('Agg') # Используем Agg для headless окружения
import matplotlib.pyplot as plt

def resize_image(input_path, output_path, scale):
    """Изменяет размер изображения на заданный коэффициент."""
    with Image.open(input_path) as img:
        new_size = (int(img.width * scale), int(img.height * scale))
        resized = img.resize(new_size, Image.Resampling.LANCZOS)
        resized.save(output_path)

def create_histogram(image_path, output_path):
    """Строит гистограмму RGB каналов и сохраняет как PNG."""
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        r, g, b = img.split()
        r_data = np.array(r).flatten()
        g_data = np.array(g).flatten()
        b_data = np.array(b).flatten()

        plt.figure(figsize=(8, 4))
        plt.hist(r_data, bins=256, color='red', alpha=0.5, label='Red', range=(0,256))
        plt.hist(g_data, bins=256, color='green', alpha=0.5, label='Green', range=(0,256))
        plt.hist(b_data, bins=256, color='blue', alpha=0.5, label='Blue', range=(0,256))
        plt.xlabel('Intensity')
        plt.ylabel('Frequency')
        plt.title('RGB Histogram')
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_path, dpi=100)
        plt.close()