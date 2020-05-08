import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf

def predict_multiclass(model, data, index):
    '''
    Make predictions using multi-class model.

    Args:
        model: model that outputs logits.
        datga: input data.
        index: index used for DataFrame

    Returns:
        DataFrame with ('pred_logits', 'pred_proba', 'pred_class') columns.
    '''

    logits = model.predict(data)
    predictions = tf.nn.softmax(logits).numpy()
    df_result = pd.DataFrame(
        {
            'pred_logits': list(logits),
            'pred_proba': list(predictions),
            'pred_class': np.argmax(predictions, axis=1)
        },
        index=index)
    return df_result

def predict_binary(model, data, index):
    '''
    Make predictions using binary model.

    Args:
        model: model that outputs logits.
        datga: input data.
        index: index used for DataFrame

    Returns:
        DataFrame with ('pred_logits', 'pred_proba', 'pred_class') columns.
    '''

    logits = model.predict(data).squeeze()
    predictions = tf.nn.sigmoid(logits).numpy()
    df_result = pd.DataFrame(
        {
            'pred_logits': logits,
            'pred_proba': predictions,
            'pred_class': predictions > .5
        },
        index=index)
    return df_result

def show_images_each_class(df, n_rows=2, n_cols=5):
    '''
    Show images from each class

    Args:
        df: pd.DataFrame with ('class_label', 'filepath') columns.
    '''

    for class_label, group in df.groupby('class_label'):
        print(class_label)
        for i, row in enumerate(group.sample(n=n_rows * n_cols).itertuples()):
            plt.subplot(n_rows, n_cols, i + 1)
            image = Image.open(row.filepath)
            row.filepath
            plt.imshow(image, cmap='gray' if image.mode=='L' else None)
            plt.axis('off')
        plt.tight_layout()
        plt.show()