
import json
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()

myText = "Risk management is key for attaining the desired levels of development.  The small island is under constant (though foreseeable) threat from external challenges (internal obstacles seem to have been edited out for simplification).  Risk management allowed us to prepare for shocks while continuing development at a steady, incremental rate. Researching the incoming comets was incredibly useful, but took up valuable time.  This was mitigated was starting development on a number of pods and then using the intervening time from inception to completion for risk management activities.  Otherwise idle time was used for study, and for some time dedicated to protection.  The amount of time dedicated to protection was limited by both time and the extra resources available.  After accumulating enough cash for a particular upgrade, any leftover could be dedicated to flood preparation. Insurance was particularly challenging, being reasonably inexpensive at the early levels of development, but more and more expensive as higher levels of development were achieved.  This price was often foregone to focus on other areas of risk management, honing in particularly on comets with a high severity and high likelihood of striking.  Smaller comets were often deemed worth the risk of strike, particularly at higher levels of achievement of when multiple comets were threatening.   The damage from these smaller comets was easy to minimize by utilizing efficient community connections.  In fact, community connections were incredibly useful for minimizing damage after a strike they became a key (and relied upon) component of risk preparation. I played through the game twice.  The first had a steep learning curve, where I greatly underestimated the amount of time necessary to achieve sufficient levels of development.  I spent too much time on preparing for risks, leisurely constructing buildings before I realized that they were not going to be completed in a timely fashion.  The second time, speed became key, and the first several levels went much more smoothly.  However, at a high enough level, it was quite difficult to reach the appointed development levels, no such much from dealing with risk, but because upgrading was so very expensive. This plateau is not something I had expected. I would offer two suggestions to help with this challenge: an option to dedicate time to speed up construction (similar to the research feature) and/or an option to take loans out at interest to pay for new constructions, more closely mirroring real life."

op = {"sentiment": 1}
response = alchemyapi.keywords("text", myText, op)
with open('aasentiment.json', 'w') as f:
	json.dump(response, f, ensure_ascii = False, indent = 4)

# response = alchemyapi.sentiment_targeted("text", myText, "comets")
# print "Sentiment: ", response["docSentiment"]["type"]
# print response
