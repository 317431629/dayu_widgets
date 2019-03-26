#!/usr/bin/env python
# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2019.3
# Email : muyanru345@163.com
###################################################################

from dayu_widgets.MLabel import MLabel
from dayu_widgets.MToolButton import MToolButton
from dayu_widgets.MComboBox import MComboBox
from dayu_widgets.MDivider import MDivider
from dayu_widgets.MFieldMixin import MFieldMixin
from dayu_widgets.MMenu import MMenu
from dayu_widgets import dayu_theme
from dayu_widgets.MAbstractSpinBox import MSpinBox
from dayu_widgets.qt import *
import math
import functools


class MPage(QWidget, MFieldMixin):
    sig_current_page_changed  = Signal(int)
    def __init__(self, parent=None):
        super(MPage, self).__init__(parent)
        size = dayu_theme.size.small
        self.register_field('page_size_selected', 25)
        self.register_field('page_size_list', [{'label': '25 - Fastest', 'value': 25},
                                               {'label': '50 - Fast', 'value': 50},
                                               {'label': '75 - Medium', 'value': 75},
                                               {'label': '100 - Slow', 'value': 100}])
        self.register_field('total', 1)
        self.register_field('current_page', 1)
        self.register_field('total_page',
                            lambda: math.ceil(1.0 * self.field('total') / self.field('page_size_selected')))
        self.register_field('display_text', lambda: '{start} - {end} of {total}'.format(
            start=self.field('current_page') * self.field('page_size_selected') + 1,
            end=min(self.field('total'), (self.field('current_page') + 1) * self.field('page_size_selected')),
            total=self.field('total')))
        self.register_field('can_pre', lambda: self.field('current_page') > 1)
        self.register_field('can_next', lambda: self.field('current_page') < self.field('total_page'))
        menu1 = MMenu(parent=self)

        self._display_label = MLabel()
        self._display_label.setAlignment(Qt.AlignCenter)
        self._change_page_size_button = MComboBox(size=size)
        self._change_page_size_button.setFixedWidth(100)
        self._change_page_size_button.set_menu(menu1)
        self._change_page_size_button.set_formatter(lambda x: u'{} per page'.format(x))

        self._pre_button = MToolButton(type=MToolButton.IconOnlyType, icon=MIcon('left_fill.svg'), size=size)
        self._pre_button.clicked.connect(functools.partial(self._slot_change_current_page, -1))
        self._next_button = MToolButton(type=MToolButton.IconOnlyType, icon=MIcon('right_fill.svg'), size=size)
        self._next_button.clicked.connect(functools.partial(self._slot_change_current_page, 1))
        self._current_page_spin_box = MSpinBox(size=size)
        self._current_page_spin_box.setMinimum(1)
        self._current_page_spin_box.valueChanged.connect(self.sig_current_page_changed)
        self._total_page_label = MLabel()

        self.bind('page_size_list', menu1, 'data')
        self.bind('page_size_selected', menu1, 'value', signal='sig_value_changed')
        self.bind('page_size_selected', self._change_page_size_button, 'value', signal='sig_value_changed')
        self.bind('current_page', self._current_page_spin_box, 'value', signal='valueChanged')
        self.bind('total_page', self._current_page_spin_box, 'maximum')
        self.bind('total_page', self._total_page_label, 'text')
        self.bind('display_text', self._display_label, 'text')
        self.bind('can_pre', self._pre_button, 'enabled')
        self.bind('can_next', self._next_button, 'enabled')

        main_lay = QHBoxLayout()
        main_lay.setSpacing(2)
        main_lay.addStretch()
        main_lay.addWidget(self._display_label)
        main_lay.addStretch()
        main_lay.addWidget(MLabel.help('|'))
        main_lay.addWidget(self._change_page_size_button)
        main_lay.addWidget(MLabel.help('|'))
        main_lay.addWidget(self._pre_button)
        main_lay.addWidget(MLabel('Page'))
        main_lay.addWidget(self._current_page_spin_box)
        main_lay.addWidget(MLabel('/'))
        main_lay.addWidget(self._total_page_label)
        main_lay.addWidget(self._next_button)
        self.setLayout(main_lay)

    def set_total(self, value):
        self.set_field('total', value)

    def _slot_change_current_page(self, offset):
        self.set_field('current_page', self.field('current_page') + offset)

    def set_page_config(self, data_list):
        self.set_field('page_size_list',
                       [{'label': str(data), 'value': data} if isinstance(data, int) else data for data in data_list])