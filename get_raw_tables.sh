#!/bin/bash

RAW_DIR=./raw


# MAST tables.

KOI_LOCAL=${RAW_DIR}/koiTable_2012Feb26.txt
if [ ! -f ${KOI_LOCAL} ]; then
    echo "Downloading KOI table..."
    curl -o ${KOI_LOCAL} http://archive.stsci.edu/pub/kepler/catalogs/koiTable_2012Feb26.txt
fi

KIC_TABLE=${RAW_DIR}/kic.txt
KIC_LOCAL=${KIC_TABLE}.gz
if [ ! -f ${KIC_TABLE} ]; then
    if [ ! -f ${KIC_LOCAL} ]; then
        echo "Downloading KIC table..."
        curl -o ${KIC_LOCAL} http://archive.stsci.edu/pub/kepler/catalogs/kic.txt.gz
    fi

    echo "Extracting KIC table (this hurts a little)..."
    gzip -d ${KIC_LOCAL}
fi


# Dressing tables.

DRESSING_STARS_LOCAL=${RAW_DIR}/dressing_stars.txt
if [ ! -f ${DRESSING_STARS_LOCAL} ]; then
    echo "Downloading Dressing 'cool stars' table..."
    curl -o ${DRESSING_STARS_LOCAL} http://arxiv.org/src/1302.1647v2/anc/tab4.txt
fi

DRESSING_KOIS_LOCAL=${RAW_DIR}/dressing_kois.txt
if [ ! -f ${DRESSING_KOIS_LOCAL} ]; then
    echo "Downloading Dressing 'KOIs' table..."
    curl -o ${DRESSING_KOIS_LOCAL} http://arxiv.org/src/1302.1647v2/anc/tab5.txt
fi
