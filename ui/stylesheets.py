main_Style='''
            QWidget {
                background-color: #EEE2DE;
            }
            QLabel {
                color: #333;
            }



QPushButton:hover {
    background-color: #cc0000; /* Darker color on hover */
}


         
    QTableWidget {
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    QTableWidget::item {
                padding: 0px;
                margin: 0px;
                alignment:center;
    }
QHeaderView::section {
        background-color: #3C486B; /* Set the background color of the header */
        color: white; /* Set the text color of the header */
        padding: 8px; /* Add padding to the header section */
        border:1px;
    }
QComboBox {
        padding: 4px;
        border: 2px solid #ccc;
        border-radius: 5px;
        background-color: #fff;
        selection-background-color: #ff0000;
        color: #333;
        text-align: center;
    }
QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left-width: 1px;
        border-left-color: #ccc;
        border-left-style: solid;
    }
        '''
header_Style='''
            QLabel {
                color: #2B2A4C;
                font-size: 29px;
                font-weight: bold;
                text-transform: uppercase;
                padding: 10px;
            }
        '''
close_Botton_Style='''
            QPushButton {
                background-color: #ff4c4c;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #e60000;
            }
        '''
heade_Label_Style='''
            QLabel {
                color: white;
                font-size: 29px;
                qproperty-alignment: AlignCenter; /* Center align the text */
            }
        '''

search_botton_style="""
    QPushButton {
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        background-color: #B31312;
        color: #fff;
    }
    QPushButton:pressed {
        background-color: #801010; /* Darker color when button is pressed */
    }
    QPushButton:released {
        background-color: #B31312; /* Restore the original color when button is released */
    }
"""
table_style="""QScrollBar:vertical {"
    "    border: none;"
    "    background: #f3f3f3;"
    "    width: 10px;"
    "    margin: 0px 0px 0px 0px;"
    "}"
    "QScrollBar::handle:vertical {"
    "    background: #c0c0c0;"
    "    min-height: 0px;"
    "}"
    "QScrollBar::add-line:vertical {"
    "    height: 0px;"
    "    subcontrol-position: bottom;"
    "    subcontrol-origin: margin;"
    "}"
    "QScrollBar::sub-line:vertical {"
    "    height: 0px;"
    "    subcontrol-position: top;"
    "    subcontrol-origin: margin;"
    "}"""
download_botton_style="""
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                background-color: #B31312;
                color: #fff;
            }
        """
download_audio_style="""
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                background-color: #7071E8;
                color: #fff;
            }
        """