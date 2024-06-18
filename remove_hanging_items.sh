#!/bin/bash
#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

SESSION_POS=5 # Position der Session ID in session.app.log
ITEM_POS=12   # Position der Item ID in session.app.log
HANGING_ITEMS="hanging_items.txt"

STEP2_MARKER="Step 2"
STEP2_LIST="step2.txt"
STEP3_MARKER="Step 3"
STEP3_LIST="step3.txt"

# Extract hanging Items from Log file
grep "$STEP2_MARKER" $1 | cut -d ' ' -f $SESSION_POS,$ITEM_POS | sort > $STEP2_LIST
grep "$STEP3_MARKER" $1 | cut -d ' ' -f $SESSION_POS,$ITEM_POS | sort > $STEP3_LIST
diff $STEP2_LIST $STEP3_LIST | grep "< " | cut -d ' ' -f 3 > $HANGING_ITEMS

# Delete hanging Items
while read line 
do 
    python remove_item.py $line
done < $HANGING_ITEMS

# Remove temporary files
rm $STEP2_LIST $STEP3_LIST $HANGING_ITEMS
