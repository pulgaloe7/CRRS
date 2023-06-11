import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO

cards_map = {
    'Knight': 'https://api-assets.clashroyale.com/cards/300/jAj1Q5rclXxU9kVImGqSJxa4wEMfEhvwNQ_4jiGUuqg.png',
    'Archers': 'https://api-assets.clashroyale.com/cards/300/W4Hmp8MTSdXANN8KdblbtHwtsbt0o749BbxNqmJYfA8.png',
    'Goblins': 'https://api-assets.clashroyale.com/cards/300/X_DQUye_OaS3QN6VC9CPw05Fit7wvSm3XegXIXKP--0.png',
    # ... Resto de las URL de las imágenes ...
}


def show_images():
    # Crea una nueva ventana para mostrar las imágenes
    image_window = tk.Toplevel(root)

    # Configura el administrador de geometría grid
    image_window.grid()

    # Variable para realizar un seguimiento del número de columnas
    column_count = 0

    # Itera sobre las claves y enlaces del cards_map
    for card_name, image_url in cards_map.items():
        # Obtiene la imagen desde la URL
        response = requests.get(image_url)
        image_data = response.content

        # Crea una imagen PIL desde los datos descargados
        pil_image = Image.open(BytesIO(image_data))

        # Cambia el tamaño de la imagen si es necesario
        pil_image = pil_image.resize((100, 100), Image.ANTIALIAS)

        # Crea una instancia de ImageTk para mostrar la imagen en Tkinter
        image = ImageTk.PhotoImage(pil_image)

        # Crea una etiqueta para mostrar la imagen
        image_label = tk.Label(image_window, image=image)
        image_label.grid(row=0, column=column_count, padx=10, pady=10)

        # Incrementa el número de columnas
        column_count += 1

        # Almacena una referencia a la imagen para evitar que se recolecte el basurero
        image_label.image = image


root = tk.Tk()

show_images_button = tk.Button(root, text="Show Images", command=show_images)
show_images_button.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
