# -*- coding: utf-8 -*-
"""
Create layouts - grids, repeats, sequences and tracks - for pyprototypr
"""
# lib
import copy
import logging
import math

# third party
import jinja2
# local
from pyprototypr.utils import tools  # geoms,
from pyprototypr.utils.tools import DatasetType
from pyprototypr.base import BaseShape
from pyprototypr.layouts import SequenceShape
from pyprototypr.shapes import (
    CircleShape, HexShape, ImageShape, RectangleShape,  SquareShape)
from pyprototypr.utils.support import LookupType

from pyprototypr import globals

log = logging.getLogger(__name__)

DEBUG = False

# ---- Functions


class Switch:
    """
    Decide if to use an element or a value for a card attribute.

    Note:
        * This class is instantiated in the `proto` module, via a script's call
          to the S() function.
        * The class __call__ is accessed via the CardShape draw_card() method
    """

    def __init__(self, **kwargs):
        self.switch_template = kwargs.get("template", None)
        self.result = kwargs.get("result", None)  # usually a Shape
        self.alternate = kwargs.get("alternate", None)  # usually a Shape
        self.dataset = kwargs.get("dataset", [])
        self.members = []  # card IDs, of which the affected card is a member

    def __call__(self, cid):
        """Process the test, for a given card 'ID' in the dataset."""
        record = self.dataset[cid]  # dict data for chosen card
        try:
            outcome = self.switch_template.render(record)
            # print('  +++', f'{ID=} {self.test} {outcome=}')
            boolean = tools.as_bool(outcome)
            if boolean:
                return self.result
            else:
                return self.alternate
        except jinja2.exceptions.UndefinedError as err:
            tools.feedback(
                f'Switch "{self.test}" is incorrectly constructed ({err})', True)
        except Exception as err:
            tools.feedback(
                f'Switch "{self.test}" is incorrectly constructed ({err})', True)
        return None


class Lookup:
    """Enable lookup of data in a record of a dataset

    Kwargs:
        lookup: Any
            the lookup column whose value must be used for the match
        target: str
            the name of the column of the data being searched
        result: str
            name of result column containing the data to be returned
        default: Any
            the data to be returned if no match is made

    In short:
        lookup and target enable finding a matching record in the dataset;
        the data in the 'result' column of that record will be returned.

    Note:
        This class will be instantiated in the `proto` module, via a
        script's call to the L() function.
    """

    def __init__(self, **kwargs):
        self.data = kwargs.get("datalist", [])
        self.lookup = kwargs.get("lookup", '')
        self.members = []  # card IDs, of which the affected card is a member

    def __call__(self, cid):
        """Return datalist item number 'ID' (card number)."""
        log.debug("datalist:%s cid:%s", self.datalist, cid)
        try:
            return None
        except (ValueError, TypeError, IndexError):
            return None

# ---- Deck / Card related


class CardShape(BaseShape):
    """
    Card shape on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CardShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # tools.feedback(f'*** CardShape {kwargs=}')
        self.elements = []  # container for objects which get added to the card
        if kwargs.get("_is_countersheet", False):
            default_height = 2.54
            default_width = 2.54
        else:
            default_height = 8.8
            default_width = 6.3
        self.height = kwargs.get("height", default_height)
        self.width = kwargs.get("width", default_width)
        self.kwargs.pop("width", None)
        self.kwargs.pop("height", None)
        self.image = kwargs.get('image', None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        raise NotImplementedError

    def draw_card(self, cnv, row, col, cid, **kwargs):
        """Draw a card on a given canvas."""
        # tools.feedback(f"\n\nCard {row=} {col=} {cid=} {self.shape=}")
        image = kwargs.get('image', None)
        # ---- draw outline
        label = "ID:%s" % cid if self.show_id else ""
        if self.shape == "rectangle":
            outline = RectangleShape(
                label=label,
                height=self.height,
                width=self.width,
                canvas=cnv,
                col=col,
                row=row,
                **self.kwargs,
            )
            outline.draw()
        elif self.shape == "square":
            outline = SquareShape(
                label=label,
                height=self.height,
                width=self.width,
                canvas=cnv,
                col=col,
                row=row,
                **self.kwargs,
            )
            outline.draw()
        elif self.shape == "circle":
            self.height = self.radius * 2.0
            self.width = self.radius * 2.0
            self.kwargs["radius"] = self.radius
            outline = CircleShape(
                label=label, canvas=cnv, col=col, row=row, **self.kwargs
            )
            outline.draw()
        elif self.shape == "hexagon":
            self.height = self.side * math.sqrt(3.0)
            self.width = self.side * 2.0
            self.kwargs["side"] = self.side
            outline = HexShape(label=label, canvas=cnv, col=col, row=row, **self.kwargs)
            outline.draw(is_cards=True)
        else:
            tools.feedback("Unable to draw a {self.shape}-shaped card.", stop=True)
        # ---- draw card elements
        flat_elements = tools.flatten(self.elements)
        for index, flat_ele in enumerate(flat_elements):
            # tools.feedback(f'*** {index=} {flat_ele=}', False)
            # ---- * replace image source placeholder
            if image and isinstance(flat_ele, ImageShape):
                #tools.feedback(f'*** {image=}', False)
                if flat_ele.kwargs.get('source', '').lower() in ['*', 'all']:
                    flat_ele.source = image

            members = self.members or flat_ele.members
            # tools.feedback(f' *** {members=}', False)
            try:
                # ---- * normal element
                iid = members.index(cid + 1)
                # tools.feedback(f"  *** {index=} {iid=} {flat_ele=} / {col=} {self.width=} / {row=} {self.height=}")
                new_ele = self.handle_custom_values(flat_ele, cid)  # calculated values
                new_ele.draw(
                    cnv=cnv, off_x=col * self.width, off_y=row * self.height, ID=iid
                )
            except AttributeError:
                # ---- * switch ... get a new element ... or not!?
                # print(f"  ^^^ {self.shape_id=}  {flat_ele=}")
                new_ele = flat_ele(cid=self.shape_id) if flat_ele else None # uses __call__ on Switch
                if new_ele:
                    flat_new_eles = tools.flatten(new_ele)
                    # print(f"    ~~~ {flat_new_eles=}")
                    for flat_new_ele in flat_new_eles:
                        # print(f"      --- PRE  --- {flat_new_ele=}")
                        members = flat_new_ele.members or self.members
                        iid = members.index(cid + 1)
                        custom_new_ele = self.handle_custom_values(flat_new_ele, iid)  # calculate
                        # print(f"      --- POST --- {custom_new_ele=}")
                        if isinstance(custom_new_ele, SequenceShape):
                            custom_new_ele.deck_data = self.deck_data
                        custom_new_ele.draw(
                            cnv=cnv,
                            off_x=col * self.width,
                            off_y=row * self.height,
                            ID=iid,
                        )
            except Exception as err:
                tools.feedback(f"Unable to draw card #{cid + 1}. (Error:{err})")


class DeckShape(BaseShape):
    """
    Placeholder for the deck design; list of CardShapes and Shapes.

    NOTE: draw() is called via the Deck function in proto.py
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(DeckShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # tools.feedback(f'*** DeckShape {kwargs=}')
        # ---- cards
        self.deck = []  # container for CardShape objects
        if kwargs.get("_is_countersheet", False):
            default_items = 70
            default_height = 2.54
            default_width = 2.54
        else:
            default_items = 9
            default_height = 8.8
            default_width = 6.3
        self.counters = kwargs.get("counters", default_items)
        self.cards = kwargs.get("cards", self.counters)  # default total number of cards
        self.height = kwargs.get("height", default_height)  # OVERWRITE
        self.width = kwargs.get("width", default_width)  # OVERWRITE
        # ---- dataset (list of dicts)
        self.dataset = kwargs.get("dataset", None)
        self.set_dataset()  # globals override : dataset AND cards
        if self.dataset:
            self.cards = len(self.dataset)
        # ---- behaviour
        self.sequence = kwargs.get("sequence", [])  # e.g. "1-2" or "1-5,8,10"
        self.template = kwargs.get("template", None)
        self.skip = kwargs.get("skip", None)
        if self.skip and not self.dataset:
            tools.feedback('Cannot set "skip" for a Deck without any existing Data!',
                           True)
        # ---- user provided-rows and -columns
        self.card_rows = kwargs.get("rows", None)
        self.card_cols = kwargs.get("cols", kwargs.get("columns", None))
        # ---- data file
        self.data_file = kwargs.get("data", None)
        self.data_cols = kwargs.get("data_cols", None)
        self.data_rows = kwargs.get("data_rows", None)
        self.data_header = kwargs.get("data_header", True)
        # ---- images dir and filter
        self.images = kwargs.get("images", None)
        self.images_filter = kwargs.get("images_filter", None)
        self.image_list = []
        # ---- FINALLY...
        self.cards += globals.extra
        self.create(self.cards)

    def set_dataset(self):
        """Create deck dataset from globals dataset"""
        if globals.dataset_type in [
                DatasetType.DICT, DatasetType.FILE, DatasetType.MATRIX]:
            log.debug("globals.dataset_type: %s", globals.dataset_type)
            if len(globals.dataset) == 0:
                tools.feedback("The provided data is empty or cannot be loaded!", True)
            else:
                # globals.deck.create(len(globals.dataset) + globals.extra)
                self.dataset = globals.dataset
        elif globals.dataset_type == DatasetType.IMAGE:
            # OVERWRITE total number of cards
            self.cards = len(globals.image_list)
        else:
            pass  # no Data created

    def create(self, cards: int = 0):
        """Create a new Deck of CardShapes, based on number of `cards`"""
        log.debug("Cards are: %s", self.sequence)
        self.deck = []
        log.debug("Deck => %s cards with kwargs: %s", cards, self.kwargs)
        for card in range(0, cards):
            _card = CardShape(**self.kwargs)
            _card.shape_id = card
            self.deck.append(_card)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Method called by Save() in proto.

        Kwargs:
            * cards - number of cards in Deck
            * image_list - list of image filenames
        """
        cnv = cnv if cnv else self.canvas
        log.debug("Deck cnv:%s type:%s", type(self.canvas), type(cnv))
        # ---- handle kwargs
        images = kwargs.get('image_list', [])
        cards = kwargs.get('cards', None)
        # ---- user-defined rows and cols
        max_rows = self.card_rows
        max_cols = self.card_cols
        # ---- calculate rows/cols based on page size and margins
        margin_left = self.margin_left if self.margin_left is not None else self.margin
        margin_bottom = self.margin_bottom if self.margin_bottom is not None else self.margin
        margin_right = self.margin_right if self.margin_right is not None else self.margin
        margin_top = self.margin_top if self.margin_top is not None else self.margin
        if not max_rows:
            row_space = float(self.page_height) - margin_bottom - margin_top
            max_rows = int(row_space / float(self.height))
        if not max_cols:
            col_space = float(self.page_width) - margin_left - margin_right
            max_cols = int(col_space / float(self.width))
        log.debug("w:%s cs:%s mc:%s", self.page_width, col_space, max_cols)
        log.debug("h:%s rs:%s mr:%s", self.page_height, row_space, max_rows)
        row, col = 0, 0
        # ---- draw cards
        for key, card in enumerate(self.deck):
            image = images[key] if images and key <= len(images) else None
            card.deck_data = self.dataset
            skip = False
            if self.skip:
                _check = tools.eval_template(self.skip, self.dataset[key], label='skip')
                skip = tools.as_bool(_check, label='skip', allow_none=False)
                # print(f'{key=} :: {self.dataset[key]=}, {skip=}')
                if not isinstance(skip, bool):
                    tools.feedback(
                        'The "skip" test must result in True or False value!', True)
            if not skip:
                card.draw_card(
                    cnv, row=row, col=col, cid=card.shape_id, image=image)
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
                if row >= max_rows:
                    row, col = 0, 0
                    if key + 1 != len(self.deck):
                        cnv.canvas.showPage()

    def get(self, cid):
        """Return a card based on the internal ID"""
        for card in self.deck:
            if card.shape_id == cid:
                return card
        return None

    def count(self):
        """Return number of cards in the deck"""
        return len(self.deck)
