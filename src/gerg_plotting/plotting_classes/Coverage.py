import matplotlib.axes
import matplotlib.colors
import matplotlib.figure
import matplotlib.patches
import matplotlib.text
import matplotlib
from matplotlib.patches import Rectangle,FancyArrow
from attrs import define,field


@define(auto_attribs=True)
class Coverage:
    """
    Encapsulates a rectangle, its outline, associated text, and range arrows.
    """
    rect: Rectangle
    rect_outline: Rectangle
    text: matplotlib.text.Text
    left_arrow: FancyArrow
    right_arrow: FancyArrow
    
    @staticmethod
    def create(anchor_point, width, height, label, 
            alpha, linewidth, edgecolor, fc, coverage_outline_alpha, 
            hatch, fontsize, label_position, arrow_width, arrow_facecolor,
            arrow_head_width, arrow_length_includes_head, arrow_zorder,
            arrow_edge_color, arrow_linewidth, arrow_text_padding, text_padding, 
            text_bbox_coords, rect_bbox_coords, **kwargs):
        """
        Factory method to create a Coverage instance, calculating arrows without plotting.

        Args:
            anchor_point (tuple): Bottom-left corner of the rectangle.
            width (float): Width of the rectangle.
            height (float): Height of the rectangle.
            label (str): Text label for the rectangle.
            alpha (float): Alpha value for rectangle fill.
            linewidth (float): Line width for outline.
            edgecolor (str): Color of the outline.
            fc (str): Fill color for the rectangle.
            coverage_outline_alpha (float): Alpha value for the outline rectangle.
            hatch (str): Hatch pattern for the rectangle.
            fontsize (int): Font size for the label text.
            label_position (tuple): Position for the label text.
            arrow_width (float): Width of the arrows.
            arrow_facecolor (str): Fill color for the arrows.
            arrow_head_width (float): Width of the arrowhead.
            arrow_length_includes_head (bool): Whether the arrow length includes the head.
            arrow_zorder (float): Z-order for the arrows.
            arrow_edge_color (str): Edge color for the arrows.
            arrow_linewidth (float): Line width for the arrows.
            arrow_text_padding (float): Padding between the arrows and the text.
            text_bbox_coords (tuple): Bounding box coordinates of the text in data coordinates.
            rect_bbox_coords (tuple): Bounding box coordinates of the rectangle in data coordinates.
            **kwargs: Additional keyword arguments for the rectangle and text.

        Returns:
            Coverage: A new instance of the class with calculated arrows.
        """
        rect = Rectangle(anchor_point, width=width, height=height,
                        fc=fc, alpha=alpha, linewidth=linewidth,
                        edgecolor=None, label=label, hatch=hatch, **kwargs)

        rect_outline = Rectangle(anchor_point, width=width, height=height, 
                                fc=None, fill=False, alpha=coverage_outline_alpha,
                                linewidth=linewidth, edgecolor=edgecolor,
                                label=None, zorder=1, **kwargs)

        text = matplotlib.text.Text(*label_position, text=label, fontsize=fontsize,
                                    ha='center', va='center', zorder=5, **kwargs)

        if arrow_facecolor == 'coverage_facecolor':
            arrow_facecolor = rect.get_facecolor()

        # Extract data coordinates for bounding boxes
        text_left, text_bottom = text_bbox_coords[0]
        text_right, text_top = text_bbox_coords[1]
        text_y_center = (text_bottom + text_top) / 2

        rect_left, _ = rect_bbox_coords[0]
        rect_right, _ = rect_bbox_coords[1]

        left_arrow_length = rect_left - text_left - 0.01
        right_arrow_length = rect_right - text_right - 0.01

        arrow_props = {
            'width': arrow_width,
            'facecolor': arrow_facecolor,
            'head_width': arrow_head_width,
            'length_includes_head': arrow_length_includes_head,
            'zorder': arrow_zorder,
            'edgecolor': arrow_edge_color,
            'linewidth': arrow_linewidth
        }

        left_arrow = FancyArrow(
            x=text_left - (arrow_text_padding - 0.03),
            y=text_y_center,
            dx=left_arrow_length + arrow_text_padding,
            dy=0,
            **arrow_props
        )

        right_arrow = FancyArrow(
            x=text_right + arrow_text_padding,
            y=text_y_center,
            dx=right_arrow_length - arrow_text_padding,
            dy=0,
            **arrow_props
        )

        return Coverage(rect, rect_outline, text, left_arrow, right_arrow)


    def format_coverage_label(self, text: matplotlib.text.Text, pad, linewidth, alpha):
        """
        Formats the coverage label with a background matching the rectangle's face color.

        Args:
            text (matplotlib.text.Text): The label text.
            pad (float): Padding around the text.
            linewidth (float): Line width for the text background.
            alpha (float): Alpha value for the text background.
        """
        text.set_bbox({
            'facecolor': self.rect.get_facecolor(),
            'pad': pad,
            'linewidth': linewidth,
            'alpha': alpha
        })

