from aqt import mw
import time
from aqt.utils import tooltip
from aqt import gui_hooks

config = mw.addonManager.getConfig(__name__)
now = time.time()
buryInterval = config.get("buryInterval", 1)

def autobury(self, c):
    # pprint(dir(mw.col.sched))
    toBury = set()
    checked = set()
    count = 0
    mw.col.add_custom_undo_entry("Undo auto bury")
    undostep = mw.col.undo_status().last_step
    for i in range(10000):
        # mw.col.reset()
        cards = mw.col.sched.get_queued_cards(fetch_limit=10000).cards
        for item in cards:
            if (item.card.id in checked):
                continue
            checked.add(item.card.id)
            card = mw.col.get_card(item.card.id)
            did = card.did
            if (card.odid):
                did = card.odid
            newbury = mw.col.decks.config_dict_for_deck_id(did)["new"].get("bury", True)
            revbury = mw.col.decks.config_dict_for_deck_id(did)["rev"].get("bury", True)
            if ((card.queue == 0 and newbury) or (card.queue == 2 and revbury)):
                for cid, queue in mw.col.db.execute(
                        f"""select id, queue from cards where nid=? and id!=?""",
                        card.nid,
                        card.id,
                ):
                    delta = (now - mw.col.card_stats_data(cid).latest_review) / 60 / 60 / 24
                    if (delta < buryInterval):
                        toBury.add(card.id)
        # print( len(toBury))
        if (len(toBury) == 0):
            break
        mw.col.sched.bury_cards(toBury, manual=False)
        count += len(toBury)
        toBury.clear()
    # print(checked)
    mw.col.merge_undo_entries(undostep)
    mw.update_undo_actions()
    tooltip("bury " + str(count) + " card(s)")

gui_hooks.overview_will_render_content.append(autobury)