import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
from sklearn import metrics
import tqdm
import time

def create_dataset_df(data_root, class_labels, image_ext):
    '''
    Create DataFrame of image dataset based on image files.

    Args:
        data_root: root directory of the image dataset
        class_labels: class names (directory names)
        image_ext: image file extension (e.g. '.jpg', '.png')
    Returns:
        DataFrame with ('filepath', 'class_label', 'class') columns.
    '''
    dfs = []
    for cls, class_label in enumerate(class_labels):
        df = pd.DataFrame(
            [(str(p), class_label, cls)
             for p in data_root.glob(class_label + '/*' + image_ext)],
            columns=['filepath', 'class_label', 'class'])
        dfs.append(df)
    df_dataset = pd.concat(dfs, ignore_index=True)
    return df_dataset


class ProgressBarCallback(tf.keras.callbacks.Callback):
    '''
    Nested progress with single bar

    Example:
        >>> with ProgressBarCallback(epochs, n_batches, batch_size) as pbar:
        >>>     model.fit(..., callbacks=[pbar])
    '''
    def __init__(self, epochs, n_batches, batch_size, leave=True):
        '''
        Initialize an object

        Args:
            n_epochs: # of epochs
            n_batchs: # of batchs per epoch
            batch_size: batch size
            leave: tqdm's leave argument
        '''
        self.n_epochs = epochs
        self.n_batches = n_batches
        self.batch_size = batch_size
        self.time_pbar_begin = time.time()
        self.bar = tqdm.tqdm(
            total=self.n_batches * self.batch_size,
            leave=leave,
            unit='batch',
            desc='1/{n_epochs} epoch'.format(n_epochs=self.n_epochs))

    def __enter__(self):
        return self

    @staticmethod
    def _duration2str(duration):
        if duration >= 100 * 60:  # in hours
            return '{:.02g}h'.format(duration / 360)
        elif duration >= 100:  # in mins
            return '{:.02g}m'.format(duration / 60)
        else:  # in secs
            return '{:.02g}s'.format(duration)

    def on_epoch_begin(self, epoch, logs={}):
        self.bar.reset(total=self.n_batches * self.batch_size)
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        summary = pd.DataFrame(self.logs).mean().to_dict()
        str_summary = ','.join(
            ['{}={:.03g}'.format(k, v) for k, v in summary.items()])
        duration = time.time() - self.time_pbar_begin
        duration_per_epoch = duration / (epoch + 1)
        expected_duration = self._duration2str(duration_per_epoch *
                                               self.n_epochs)
        duration_per_epoch = ProgressBarCallback._duration2str(
            duration_per_epoch)
        duration = ProgressBarCallback._duration2str(duration)
        self.bar.set_description(
            '{epoch}/{n_epochs} epoch [{duration}/{expected_duration} ({epoch_duration}/epoch) last_epoch=({summary})]'
            .format(duration=duration,
                    expected_duration=expected_duration,
                    epoch_duration=duration_per_epoch,
                    summary=str_summary,
                    epoch=epoch + 1,
                    n_epochs=self.n_epochs))

    def on_batch_begin(self, batch, logs={}):
        pass

    def on_batch_end(self, batch, logs={}):
        logs.pop('batch'), logs.pop('size')
        self.logs.append(logs)
        self.bar.update(self.batch_size)
        self.bar.set_postfix(logs)

    def __exit__(self, exc_type, exc_value, traceback):
        self.bar.close()

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

def show_images_each_class(df, n_rows=2, n_cols=5, figsize=None):
    '''
    Show images from each class

    Args:
        df: pd.DataFrame with ('class_label', 'filepath') columns.
    '''

    for class_label, group in df.groupby('class_label'):
        print(class_label)
        plt.figure(figsize=figsize)
        for i, row in enumerate(group.sample(n=n_rows * n_cols).itertuples()):
            plt.subplot(n_rows, n_cols, i + 1)
            image = Image.open(row.filepath)
            row.filepath
            plt.imshow(image, cmap='gray' if image.mode=='L' else None)
            plt.axis('off')
        plt.tight_layout()
        plt.show()

def plot_roc_curves(df_result, figsize=(3, 3)):
    '''
    Plot ROC curve(s)

    Args:
        df_result: DataFrame with ('class_label', 'pred_proba') columns
        figsize: figure size

    '''
    plt.figure(figsize=figsize)
    class_labels = df_result['class_label'].unique()
    if len(class_labels) == 2:  # binary classification
        pred_proba = [1 - df_result['pred_proba'], df_result['pred_proba']]
        enum_start = 1
        class_labels = [class_labels[1]]
    else:  # multi_class classification
        pred_proba = np.stack(df_result['pred_proba']).T
        print(pred_proba.shape)
        enum_start = 0

    for i, cls in enumerate(class_labels, enum_start):
        fpr, tpr, thresholds = metrics.roc_curve(df_result['class'] == i,
                                                 pred_proba[i])
        auc = metrics.auc(fpr, tpr)
        plt.plot(fpr,
                 tpr,
                 label='{cls} (AUC = {auc:.03g})'.format(cls=cls, auc=auc))

    plt.plot((0, 1), (0, 1), zorder=0, color='black', alpha=.1,
             linestyle='-')  # diagonal line
    plt.xlabel('1 - Specificity')
    plt.ylabel('Sensitivity')
    plt.legend(loc='lower right')

def confusion_matrix(df_result):
    '''
    Create DataFrame of confusion matrix.

    Args:
        df_result: DataFrame with ('class_label', 'class', 'pred_class') columns
    '''
    class_labels = df_result['class_label'].unique()
    cm = metrics.confusion_matrix(df_result['class'], df_result['pred_class'])
    df_cm = pd.DataFrame(cm, index=class_labels, columns=class_labels)
    df_cm.index.name, df_cm.columns.name = 'Truth', 'Prediction'
    return df_cm