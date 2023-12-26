from matplotlib import pyplot as plt
import seaborn as sns
import argparse
from src.data import results_directory


def get_parser():
    """
    Creates a parser with three arguments:
        num-redo: the number of times we want to repeat the experiment
        room-patter: the pattern of the room

    :return: the parsers arguments
    """
    parser = argparse.ArgumentParser(description='Command parser')

    parser.add_argument('--num-redo', type=int, help='Number of redo operations')
    parser.add_argument('--room-pattern', type=int, help='Room number')

    return parser.parse_args()


def plot_histogram(x_data, y_data, x_label, y_label, title, filename="", save=False,  line_plot=False):
    sns.set_context('paper')
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 7))

    if line_plot:
        sns.lineplot(x=x_data, y=y_data, marker='o', color='blue')
    else:
        ax = sns.barplot(x=x_data, y=y_data, color='blue')
        # y-axis view limits
        ax.set_ylim(-10, 115)

        # line contour in all bars
        for patch in ax.patches:
            patch.set_edgecolor('black')
            patch.set_linewidth(0.8)

    # set ticks font size
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    plt.xlabel(x_label, fontsize=15, labelpad=15)
    plt.ylabel(y_label, fontsize=15, labelpad=15)
    plt.title(title, fontsize=20, pad=20)

    if save and filename != "":
        plt.savefig(results_directory + "/{}.pdf".format(filename), bbox_inches='tight', dpi=100)

    plt.show()
