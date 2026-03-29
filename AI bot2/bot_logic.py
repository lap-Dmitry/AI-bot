import random
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

facts_pigeons = ['Шея у голубя состоит из 44 позвонков и поэтому очень подвижная, благодаря чему птица легко может менять направление полёта.',
                'Особенно развита грудная кость, на которой крепятся грудные мышцы, выполняющие важную работу при полёте. У лётных пород эти мышцы очень массивные и могут достигать 25% от общей массы тела.',
                'Голуби не имеют зубов и мочевого пузыря, которые могли бы утяжелить их при полёте.',
                'Кожа у голубей очень тонкая и сухая, хорошо развит подкожный слой. Потовые и сальные железы отсутствуют.'
                ]

facts_tits = ['Синицы — социальные птицы, часто образуют стаи, которые могут включать несколько видов. Это помогает им лучше находить пищу и защищаться от хищников.',
                'В период размножения многие виды синиц становятся территориальными и защищают свою территорию от соперников. Они используют громкое пение и другие поведенческие признаки для обозначения границ своей территории.',
                'Синицы могут запоминать местоположение своих запасов пищи — исследования показали, что они способны помнить, где именно они спрятали запасы еды на протяжении длительного времени.',
                'Большинство синиц, особенно в умеренных и субарктических регионах, — оседлые птицы и не мигрируют. В некоторых случаях, особенно в периоды дефицита пищи, синицы могут совершать небольшие перемещения в поисках еды.']

def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>123456789"
    password = ""

    for i in range(pass_length):
        password += random.choice(elements)

    return password

def gen_emodji():
    emodji = ["\U0001f600", "\U0001f642", "\U0001F606", "\U0001F923"]
    return random.choice(emodji)


def flip_coin():
    flip = random.randint(0, 2)
    if flip == 0:
        return "ОРЕЛ"
    else:
        return "РЕШКА"
    
def get_class(model_path, labels_path, image_path):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model(model_path, compile=False)

    # Load the labels
    class_names = open(labels_path, "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(image_path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    if class_name[0] == '0':
        return f'Для голубей — перловка, пшеница, ячмень, семечки, гречка, просо, горох, чечевица и другие крупы в сухом виде. Факт о голубях: {random.choice(facts_pigeons)}'
    elif class_name[0] == '1':
        return f'Для синиц - семена подсолнечника, орешки: грецкие, фундук, кедровые, кусочки сала (обязательно несоленого!). Факт о синицах: {random.choice(facts_tits)}'
    elif class_name[0] == '2':
        return 'Нет данных по загруженным объектам.'
    else:
        return 'Ошибка сервера'