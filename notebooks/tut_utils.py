import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn import metrics
import torch
import torch.nn.functional as F

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

def load_dataset(df, load_img):
    '''
    Args:
        df: pd.DataFrame with 'filepath' and 'class' columns
        load_img: function for loading images
    '''
    data = np.stack([load_img(filepath) for filepath in df['filepath']])
    labels = df['class'].tolist()
    data = data / 255
    return data.astype(np.float32), labels

def predict_multiclass(model, loader, index):
    '''
    Make predictions using multi-class model.

    Args:
        model: model that outputs logits.
        loader: input data.
        index: index used for DataFrame

    Returns:
        DataFrame with ('pred_logits', 'pred_proba', 'pred_class') columns.
    '''
    model.freeze()
    model.eval()

    ys = []
    with torch.no_grad():
        for batch in loader:
            x, _ = batch
            logits = model(x)
            ys.append(logits)
    logits = torch.cat(ys, axis=0)
    preds = F.softmax(logits, dim=1)
    preds = preds.cpu().numpy()
    df_result = pd.DataFrame({
        'logits': list(logits.cpu().numpy()),
        'pred_proba': list(preds),
        'pred_class': np.argmax(preds, axis=1)
    })
    df_result.index = index
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
            plt.imshow(image, cmap='gray' if image.mode == 'L' else None)
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


class AugmentedDataset(torch.utils.data.Dataset):
    def __init__(self, x, y, transform=None):
        self.transform = transform

        self.xs = x
        self.ys = y

    def __len__(self):
        return len(self.xs)

    def __getitem__(self, idx):
        x, y = self.xs[idx], self.ys[idx]
        if self.transform:
            x = self.transform(image=x)['image']
        x = x.transpose(2, 0, 1)  # to channel first

        return x.astype(np.float32), y