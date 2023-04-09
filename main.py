
if __name__ == '__main__':
    norm = matplotlib.colors.Normalize(vmin=0, vmax=255)
    cmap = cm.gray
    number_to_color_mapper = cm.ScalarMappable(norm=norm, cmap=cmap)
