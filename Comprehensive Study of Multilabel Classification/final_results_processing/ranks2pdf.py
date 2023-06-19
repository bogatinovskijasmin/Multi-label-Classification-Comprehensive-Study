import matplotlib.pyplot as plt
from matplotlib import rc, font_manager
import sys
import traceback
from os import makedirs
from os.path import exists


def center(width, n):
    """
    Computes free space on the figure on both sides.
    :param width:
    :param n: number of algorithms
    :return:
    """
    max_unit = 1
    free_space = width - n * max_unit
    free_space = max(0, free_space / max_unit)
    free_left = free_space / 2
    free_right = free_space / 2
    return free_left, free_right
    

def diagram(list_of_algorithms, critical_distance, the_algorithm_candidate, output_figure_file, draw_cd_line):
    """
    Draws critical distance diagram for Nemenyi or Bonferroni-Dunn post-hoc test.
    The diagram is shown if output_figure_file is None, and saved otherwise
    to the file.

    :param list_of_algorithms: [[(alg_name1, avg_rank1)], ...]
    :param critical_distance:
    :param output_figure_file: If not none, the diagram produced is saved to the specified file.
    Otherwise, the diagram is shown.
    :param the_algorithm_candidate: If we were performing Bonferroni-Dunn post-hcc test (1 vs all),
    this is the algorithm  from the list list_of_algorithms, which the other algorithms are compared to.
    If we were performing Nemenyi post-hoc test (all vs all), this should be None.
    :param draw_cd_line: boolean: whether to draw the critical distance line under the diagram or not
    :return: output_figure_file
    """

    n = len(list_of_algorithms)
    sorted_algorithms = sorted(list_of_algorithms, key=lambda t: t[1])
    the_index = None
    if the_algorithm_candidate is not None:
        for i, alg_description in enumerate(sorted_algorithms):
            if alg_description[0] == the_algorithm_candidate:
                the_index = i
                break
        if the_index is None:
            print("{} not found among the results. We will draw Nemenyi style diagram.".format(the_algorithm_candidate))
    inf = float("inf")
    deltas = [inf] + [sorted_algorithms[i + 1][1] - sorted_algorithms[i][1] for i in range(n - 1)] + [inf]
    sorted_algos_copy = sorted(list_of_algorithms, key=lambda t: t[1])
    sorted_algos_copy = sorted_algos_copy[: n//2] + sorted_algos_copy[n//2:][::-1]  # for easier drawing
    # some plot parameters:

    inter_lines_space = 0.34
    link_length_bonus = 0.04
    names_lines_space = 0.12
    first_level_height = 0.1
    critical_distance_offset = -0.88    # position of the critical distance under the main plot
    end_of_line_manipulator = 1.5        # shorten the horizontal part of the line by that much
    font_size = 23


    # JASMIN MODIFICATION
    #inter_lines_space = 0.34
    #link_length_bonus = 0.04
    #names_lines_space = 0.12
    #first_level_height = 0.1
    #critical_distance_offset = 1.4  # position of the critical distance under the main plot
    #end_of_line_manipulator = 1  # shorten the horizontal part of the line by that much
    #font_size = 15



    # latex fonts
    fontProperties = {'family': 'serif', 'serif': ['Computer Modern Roman'],
        'weight' : 'normal', 'size': font_size}
    ticks_font = font_manager.FontProperties(family='Computer Modern Roman', style='normal',
                                             size=font_size, weight='normal', stretch='normal')
    rc('text', usetex=True)
    rc('font', **fontProperties)

    def name_length(name):
        length_converter = 2
        return len(name) / length_converter + names_lines_space

    # figure dimensions
    x_min, x_max = inf, -inf
    for i, [alg_description, alg_rank] in enumerate(sorted_algos_copy):
        m = alg_rank + (2 * int(i >= n // 2) - 1) * name_length(alg_description)
        x_max = max(x_max, m)
        x_min = min(x_min, m)
    x_left = x_min
    x_right = x_max

    #x_min = min(x_min, 1)
    #x_max = max(x_max, n)

    x_min = min(x_min, 1) + 1.5
    x_max = max(x_max, n) - 1.5


    y_min = -1
    y_max = first_level_height + inter_lines_space * (1 + n//2)

    #JASMIN CHANGE FROM 16 to 8
    absolute_width, absolute_height = 10, 0.5 * n
    #absolute_width, absolute_height = 5.5, 0.01 * n



    plt.rcParams['figure.figsize'] = absolute_width, max(absolute_height, 5)
    #plt.rcParams['figure.figsize'] = absolute_width, 3.5

    left_bonus, right_bonus = center(absolute_width, n)
    # plotting
    fig = plt.figure()


    ax = fig.add_subplot(111, autoscale_on=False,
                         xlim=(x_min - 0.2 - left_bonus, x_max + 0.2 + right_bonus),
                         ylim=(y_min, max(y_max, 3)))

    def plot_algorithm(algorithm_index, algorithm, avg_rank):
        if algorithm_index < n // 2:
            # go left
            sign = -1
            offset = 0
            alignment = 'left'
            x_end_of_line = x_left + end_of_line_manipulator
        else:
            sign = 1
            offset = n // 2
            alignment = 'right'
            #x_end_of_line = x_right - end_of_line_manipulator   original matej
            x_end_of_line = x_right - end_of_line_manipulator
        line_xs = [avg_rank, avg_rank, x_end_of_line]
        height = (algorithm_index + 1 - offset) * inter_lines_space + first_level_height
        line_ys = [0, height, height]
        plt.plot(line_xs, line_ys, 'k', linewidth=1.2)
        colour = 'k' if the_algorithm_candidate != algorithm else 'b'  # index does not work here ...


        if alignment=="right":
            text_x = x_end_of_line - sign * names_lines_space
        else:
            text_x = x_end_of_line - sign * names_lines_space
        # if algorithm == "Ada300":
        #     algorithm = "AdaBoost.MH"
        # if algorithm == "RSMLCC":
        #     algorithm = "RSLP"
        #
        # if algorithm == "RAkEL2":
        #     algorithm = "RAkEL"
        #
        # if algorithm in ["RFPCT", "CDE"]:
        #     bbox = {'facecolor': 'blue', 'alpha': 0.25, 'pad': 2}
        # elif algorithm in ["RFDTBR", "ECCJ48", "EBRJ48", "CC", "AdaBoost.MH", "SSM", "MBR", "CDN", "ELPJ48"]:
        #     bbox = {'facecolor': 'blue', 'alpha': 0.5, 'pad': 2}
        # elif algorithm in ["RSLP", "EPS", "TREMLC", "RAkEL", "HOMER"]:
        #     bbox = {'facecolor': 'cyan', 'alpha': 0.5, 'pad': 2}
        # elif algorithm in ["PSt", "LP"]:
        #     bbox = {'facecolor': 'green', 'alpha': 0.25, 'pad': 2}
        # elif  algorithm in ["BR", "CLR"]:
        #     bbox = {'facecolor': 'green', 'alpha': 0.5, 'pad': 2}
        # else:
        #     bbox = {'facecolor': 'orange', 'alpha': 0.5, 'pad': 2}



        ax.text(text_x, height + names_lines_space, algorithm, bbox=bbox, horizontalalignment=alignment,     verticalalignment='center')
        #ax.text(text_x, height + names_lines_space, algorithm,
        #        horizontalalignment=alignment,
        #        verticalalignment='center',
        #        color=colour,
        #        fontsize=font_size)

    def plot_critical_distance():
        y = critical_distance_offset
        x0 = 1
        if draw_cd_line:
            plt.plot([x0, critical_distance + x0], [y, y], '|r', markersize=12, markeredgecolor='r', markeredgewidth=2)
            plt.plot([x0, critical_distance + x0], [y, y], 'r', linewidth=2)
        ax.text(x0, y + names_lines_space, "{}: {:.4f}".format("critical distance", critical_distance),
                horizontalalignment='left',
                color='r',
                fontsize=font_size)

    def algorithm_groups():
        sorted_ranks = [t[1] for t in sorted_algorithms]  # only ranks
        intervals = set()
        for start in range(len(sorted_ranks)):
            for end in range(start + 1, len(sorted_ranks)):
                if sorted_ranks[end] - sorted_ranks[start] < critical_distance:
                    if the_index is None:
                        intervals.add((start, end))
                    elif start == the_index or end == the_index:
                        intervals.add((start, end))
        found_anything = True
        while found_anything:
            found_anything = False
            unnecessary_intervals = []
            for a in intervals:
                for b in intervals:
                    if a != b and a[0] <= b[0] < b[1] <= a[1]:
                        unnecessary_intervals.append(b)
                        found_anything = True
            for unnecessary_interval in unnecessary_intervals:
                intervals -= {unnecessary_interval}
        groups = sorted(intervals, key=lambda t: t[0])
        if the_index is not None and groups:
            # only one 'interval'
            groups = [(groups[0][0], groups[-1][1])]
        return groups

    def plot_groups(intervals):
        k = len(intervals)
        start, end = 0, inter_lines_space + first_level_height
        heights = [start * (1 - t / (k + 1)) + end * t/(k + 1) for t in range(1, k + 1)]
        colours = ['|r', 'r'] if the_index is None else ['|b', 'b']
        for ind, [ind1, ind2] in enumerate(intervals):
            y = heights[ind]
            start = sorted_algorithms[ind1][1] - min(deltas[ind1], link_length_bonus)
            end = sorted_algorithms[ind2][1] + min(deltas[ind2 + 1], link_length_bonus)
            plt.plot([start, end], [y, y], colours[0], markersize=12, markeredgecolor=colours[1], markeredgewidth=1.5)
            plt.plot([start, end], [y, y], colours[1], linewidth=1)
        
    # hide 'axes box'
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    # change ticks
    plt.tick_params(
        axis='y',          # changes apply to the alg_rank-axis
        which='both',      # both major and minor ticks are affected
        left=False,        # ticks along the bottom edge are off
        right=False,       # ticks along the top edge are off
        labelleft=False)   # labels along the bottom edge are off
    plt.tick_params(
        axis='x',
        which='both',
        top=False
        )
    plt.tick_params('both', length=15, width=1, which='major')
    # line of algorithm ranks at y = 0
    ax.spines['bottom'].set_position('zero')
    # draw ticks
    plt.xticks(range(1, 1 + n), range(1, 1 + n), size=20)
    # algorithm ranks line
    plt.plot([1, n], [0, 0], 'k')
    # algorithm descriptions
    for i, alg_rank in enumerate(sorted_algos_copy):
        plot_algorithm(i, alg_rank[0], alg_rank[1])
    # critical distance
    plot_critical_distance()
    # algorithm groups
    plot_groups(algorithm_groups())
    # save / show the results
    if output_figure_file is not None:
        folder_end = output_figure_file.rfind("/")
        if folder_end >= 0:
            fig_folder = output_figure_file[:folder_end]
            if not exists(fig_folder):
                makedirs(fig_folder)
        fig.savefig(output_figure_file)
        plt.clf()
        print("Plot saved to", output_figure_file)
    else:
        plt.show()

    return output_figure_file


def remove_backslash(file_name):
    ch_list = []
    for ch in file_name:
        if ch != "\\":
            ch_list.append(ch)
        else:
            ch_list.append("/")
    return "".join(ch_list)
    
results = []
try:
    results_file = sys.argv[1].strip().split("=")[1]
    options = {"results": None, "the_algorithm": None, "out": None, "cd": False}

    for i in range(1, len(sys.argv)):
        option_name, option_value = sys.argv[i].strip().split("=")
        options[option_name] = option_value

    with open(results_file, "r") as f:
        critical_distance_value = float(f.readline().strip().split(" ")[1])
        for x in f:
            s = x.rfind(" ")
            ime, rang = x[:s], x[s + 1:]
            results.append([ime, float(rang)])
    if options["out"] is not None:
        options["out"] = remove_backslash(options["out"])
    if options["cd"] is not False:
        options["cd"] = True
    diagram(results, critical_distance_value, options["the_algorithm"], options["out"], options["cd"])
except:
    message = "Something went wrong:\n\n"
    message += traceback.format_exc()
    message += """\n
python ranks2pdf.py results=<results file> [the_algorithm=<the algorithm>] [out=<output file>]
The options are the following:

the_algorithm: name of the algorithm as it appears in results_file.
The results and output file are strings of form path/to/the/file
The results file contains lines that are of form:

<N: number of algorithms> <critical distance> <something>   # we read only the critical distance
alg_name1 avg_rank1
...
alg_nameN avg_rankN

Options in brackets are optional. For the meaning of the arguments, see the docstring of the method diagram.
"""

else:
    message = "Finnished."
finally:
    print(message)
