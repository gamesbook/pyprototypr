# -*- coding: utf-8 -*-
"""
Create layouts - grids, repeats, sequences and tracks - for pyprototypr
"""
# lib
import logging
import math

# third party
# local
from pyprototypr.utils import tools  # geoms,
from pyprototypr.base import BaseShape
from pyprototypr.shapes import (
    CircleShape, HexShape, ImageShape, RectangleShape, SquareShape)

log = logging.getLogger(__name__)

DEBUG = False

# ---- Deck / Card related  =====


class CardShape(BaseShape):
    """
    Card shape on a given canvas.
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(CardShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # tools.feedback(f'*** CardShape {kwargs=}')
        self.elements = []  # container for objects which get added to the card
        self.height = kwargs.get("height", 8.8)
        self.width = kwargs.get("width", 6.3)
        self.kwargs.pop("width", None)
        self.kwargs.pop("height", None)
        self.image = kwargs.get('image', None)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        """Draw an element on a given canvas."""
        raise NotImplementedError

    def draw_card(self, cnv, row, col, cid, **kwargs):
        """Draw a card on a given canvas."""
        # log.debug("Card r:%s c:%s id:%s shp:%s", row, col, cid, self.shape)
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
            # ---- * replace image source placeholder
            if image and isinstance(flat_ele, ImageShape):
                # tools.feedback(f'*** {image=} {flat_ele=} {flat_ele.kwargs=}')
                if flat_ele.kwargs.get('source', '').lower() in ['*', 'all']:
                    flat_ele.source = image

            members = flat_ele.members or self.members
            try:
                # ---- * normal element
                iid = members.index(cid + 1)
                # tools.feedback(f"*** {iid=} {col=} {self.width=} / {row=} {self.height=}")
                flat_ele.draw(
                    cnv=cnv, off_x=col * self.width, off_y=row * self.height, ID=iid
                )
            except AttributeError:
                # ---- * query ... get a new element ... or not!?
                log.debug("self.shape_id:%s", self.shape_id)
                new_ele = flat_ele(cid=self.shape_id)  # uses __call__ on Query
                if new_ele:
                    flat_new_eles = tools.flatten(new_ele)
                    for flat_new_ele in flat_new_eles:
                        members = flat_new_ele.members or self.members
                        iid = members.index(cid + 1)
                        flat_new_ele.draw(
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

    NOTE: draw() is called by the DeckShape
    """

    def __init__(self, _object=None, canvas=None, **kwargs):
        super(DeckShape, self).__init__(_object=_object, canvas=canvas, **kwargs)
        # tools.feedback(f'*** DeckShape {kwargs=}')
        # ---- cards
        self.deck = []  # container for CardShape objects
        self.cards = kwargs.get("cards", 9)  # default total number of cards
        self.height = kwargs.get("height", 8.8)  # OVERWRITE
        self.width = kwargs.get("width", 6.3)  # OVERWRITE
        self.sequence = kwargs.get("sequence", [])  # e.g. "1-2" or "1-5,8,10"
        self.template = kwargs.get("template", None)
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
        self.create(self.cards)

    def create(self, cards):
        """Create a new deck, based on number of `cards`"""
        log.debug("Cards are: %s", self.sequence)
        self.deck = []
        log.debug("Deck => %s cards with kwargs: %s", cards, self.kwargs)
        for card in range(0, cards):
            _card = CardShape(**self.kwargs)
            _card.shape_id = card
            self.deck.append(_card)

    def draw(self, cnv=None, off_x=0, off_y=0, ID=None, **kwargs):
        cnv = cnv if cnv else self.canvas
        log.debug("Deck cnv:%s type:%s", type(self.canvas), type(cnv))
        # ---- handle kwargs
        images = kwargs.get('image_list', [])
        cards = kwargs.get('cards', None)
        # ---- user-defined rows and cols
        max_rows = self.card_rows
        max_cols = self.card_cols
        # ---- calculate rows/cols based on page size and margins
        if not max_rows:
            row_space = float(self.page_height) - self.margin_bottom - self.margin_top
            max_rows = int(row_space / float(self.height))
        if not max_cols:
            col_space = float(self.page_width) - self.margin_left - self.margin_right
            max_cols = int(col_space / float(self.width))
        log.debug("w:%s cs:%s mc:%s", self.page_width, col_space, max_cols)
        log.debug("h:%s rs:%s mr:%s", self.page_height, row_space, max_rows)
        row, col = 0, 0
        # ---- draw cards
        for key, card in enumerate(self.deck):
            image = images[key] if images and key <= len(images) else None
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
