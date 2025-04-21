PROGRAM_FC  = """
Generate a python-like program that describes the reasoning steps required to verify the claim step-by-step. You can call three functions in the program: 1. Question() to answer a question; 2. Verify() to verify a simple claim. Several examples are given as follows.

Claim: Howard University Hospital and Providence Hospital are both located in Washington, D.C.
>>>>>>
def program():
    fact_1 = Verify("Howard University Hospital is located in Washington, D.C.")
    fact_2 = Verify("Providence Hospital is located in Washington, D.C.")
------
Claim: WWE Super Tuesday took place at an arena that currently goes by the name TD Garden.
>>>>>>
def program():
    answer_1 = Question("Which arena the WWE Super Tuesday took place?")
    fact_1 = Verify(f"{answer_1} currently goes by the name TD Garden.")
------
Claim: Talking Heads, an American rock band that was "one of the most critically acclaimed bands of the 80's" is featured in KSPN's AAA format.
>>>>>>
def program():
    fact_1 = Verify("Talking Heads is an American rock band.")
    fact_2 = Verify("Talking Heads was 'one of the most critically acclaimed bands of the 80's'.")
    fact_3 = Verify("Talking Heads is featured in KSPN's AAA format.")
------
Claim: An IndyCar race driver drove a Formula 1 car designed by Peter McCool during the 2007 Formula One season.
>>>>>>
def program():
    answer_1 = Question("Who drove the Formula 1 car designed by Peter McCool during the 2007 Formula One season?")
    fact_1 = Verify(f"{answer_1} is an Indycar race driver.")
------
Claim: Gina Bramhill was born in a village. The 2011 population of the area that includes this village was 167,446.
>>>>>>
def program():
    answer_1 = Question("Which village was Gina Bramhill born in?")
    fact_1 = Verify(f"The 2011 population of the area that includes {answer_1} was 167,446.")
------
Claim: Don Ashley Turlington graduated from Saint Joseph's College, a private Catholic liberal arts college in Standish.
>>>>>>
def program():
    fact_1 = Verify("Saint Joseph's College is a private Catholic liberal arts college")
    fact_2 = Verify("Saint Joseph's College is located in Standish")
    fact_3 = Verify(f"Don Ashley Turlington graduated from Saint Joseph's College.")
------
Claim: Gael and Fitness are not published in the same country.
>>>>>>
def program():
    answer_1 = Question("Which country was Gael published in?")
    answer_2 = Question("Which country was Fitness published in?")
------
Claim: Blackstar is the name of the album released by David Bowie that was recorded in secret.
>>>>>>
def program():
    fact_1 = Verify("David Bowie released an album called Blackstar.")
    fact_2 = Verify("David Bowie recorded an album in secret.")
------
Claim: In the 2004 Hockey film produced by a former major league baseball pitcher Kurt Russell played the USA coach.
>>>>>>
def program():
    answer_1 = Question("Which 2004 Hockey film was produced a former major league baseball pitcher?")
    fact_1 = Verify("Kurt Russell played the USA coach in the film {answer_1}.")
------
Claim: Along with the New York Islanders and the New York Rangers, the New Jersey Devils NFL franchise is popular in the New York metropolitan area.
>>>>>>
def program():
    fact_1 = Verify("The New York Islanders are popular in the New York metropolitan area.")
    fact_2 = Verify("The New York Rangers are popular in the New York metropolitan area.")
    fact_3 = Verify("The New Jersey Devils NFL franchise is popular in the New York metropolitan area.")
------
Claim: Jack McFarland is the best known role of the host of the 64th Annual Tony Awards.
>>>>>>
def program():
    answer_1 = Question("Who is the host of the 64th Annual Tony Awards?")
    fact_1 = Verify(f\"Jack McFarland is the best known role of {answer_1}.)
------
Claim: The song recorded by Fergie that was produced by Polow da Don and was followed by Life Goes On was M.I.L.F.$.
>>>>>>
def program():
    fact_1 = Verify("M.I.L.F.$ was recorded by Fergie that was produced by Polow da Don.")
    fact_2 = Verify("M.I.L.F.$ was was followed by Life Goes On.")
------
Claim: Eatza Pizza and Your Pie were not founded in the same state.
>>>>>>
def program():
    answer_1 = Question("Which state was Eatza Pizza founded in?")
    answer_2 = Question("Which state was Your Pie founded in?")
------
Claim: Gregg Rolie and Rob Tyner, are not a keyboardist.
>>>>>>
def program():
    fact_1 = Verify("Gregg Rolie is not a keyboardist.")
    fact_2 = Verify("Rob Tyner is not a keyboardist.")
------
Claim: Maria Esther Andion Bueno, not Jimmy Connors, is the player that is from Brazil.
>>>>>>
def program():
    fact_1 = Verify("Maria Esther Andion Bueno is from Brazil.")
    fact_2 = Verify("Jimmy Connors is not from Brazil.")
------
Claim: Vladimir Igorevich Arnold died after Georg Cantor.
>>>>>>
def program():
    answer_1 = Question("When did Vladimir Igorevich Arnold die?")
    answer_2 = Question("When did Georg Cantor die?")
------
Claim: Barton Mine was halted by a natural disaster not Camlaren Mine.
>>>>>>
def program():
    fact_1 = Verify("Barton Mine was halted by a natural disaster.")
    fact_2 = Verify("Camlaren Mine was not halted by a natural disaster.")
------
Claim: John O'Hara and Rabindranath Tagore are not the same nationality.
>>>>>>
def program():
    answer_1 = Question("What is the nationality of John O'Hara?")
    answer_2 = Question("What is the nationality of Rabindranath Tagore?")
------
Claim: Thomas Loren Friedman has won more Pulitzer Prizes than Colson Whitehead.
>>>>>>
def program():
    answer_1 = Question("How many Pulitzer Prizes has Thomas Loren Friedman won?")
    answer_2 = Question("How many Pulitzer Prizes has Colson Whitehead won?")
------
Claim: The model of car Trevor Bayne drives was introduced for model year 2006. The Rookie of The Year in the 1997 CART season drives it in the NASCAR Sprint Cup.
>>>>>>
def program():
    answer_1 = Question("Which model of car is drived by Trevor Bayne?")
    fact_1 = Verify(f"{answer_1} was introduced for model year 2006.")
    answer_2 = Question("Who is the Rookie of The Year in the 1997 CART season?")
    fact_2 = Verify(f"{answer_2} drives the model of car Trevor Bayne drives in the NASCAR Sprint Cup.")
------
Claim: %s
>>>>>>
"""

answer_question_gpt  = """
According to the given evidence, find the answer for the given question. If the evidence doesn't contain answer, you can properly use chatgpt's knowledge,you should give your answer anyway. All information has been given, strictly obey the answer format. Several examples are given as follows. 

Question: Which arena the WWE Super Tuesday took place?
Evidence: Super Tuesday was a 1-hour professional wrestling television special event, produced by the World Wrestling Entertainment (WWE) that took place on 12 November 2002 (which was taped November 4 & 5) at the Fleet Center in Boston, Massachusetts and Verizon Wireless Arena in Manchester, New Hampshire, which featured matches from both Raw and SmackDown. It was a preview for Survivor Series and aired on UPN.
>>>>>>
Answer: [Fleet Center in Boston, Massachusetts, Verizon Wireless Arena in Manchester, New Hampshire]
------
Question: Who drove the Formula 1 car designed by Peter McCool during the 2007 Formula One season?
Evidence: The Super Aguri F1 SA07 was Super Aguri F1's Formula One car for the 2007 Formula One season. It was designed by Peter McCool and was driven by Takuma Sato and Anthony Davidson.
>>>>>>
Answer: [Takuma Sato, Anthony Davidson]
------
Question: Which village was Gina Bramhill born in?
Evidence: Gina Bramhill was born in Eastoft, where she grew up on a farm. As a child, she appeared in several school plays. She was trained at the Royal Academy of Dramatic Art. Shortly after graduating she appeared as Bella in the movie Lotus Eaters. 2012 she got a role as the recurring character Eve Sands in the TV series Being Human. In the same year Bramhill played one of the main roles in the drama pilot The Frontier. In Coronation Street she portrayed the character Jodie Woodward. She got a main role in the movie Pleasure Island, which was shown at the Cannes Film Festival in 2014.
>>>>>>
Answer: [Eastoft]
------
Question: Which country was Gael published in?
Evidence: Bilé is a character in the "Lebor Gabála Érenn", a medieval Christian history of Ireland and the Irish (or Gaels), and in the genealogies of John O'Hart based on this tradition. He is described as a king of Galicia, an ancestor of the Gaels, the son of Breogan, and the father of Milesius. The "Lebor Gabála" purports to be an account of the Gaels' descent from Adam through the sons of Noah and how they came to Ireland. The tale relates that the Gaels spent 440 years wandering the Earth and underwent a series of tribulations, loosely based on the tale of the Israelites in the Old Testament. Eventually, the Gaels sailed to Iberia and conquered it. 
>>>>>>
Answer: [Ireland]
------
Question: Which country was Fitness published in?
Evidence: The BLV Verlag is a howto book publisher in Germany. The program includes over 600 titles, to which about 120 new books published annually. Main topic areas are the garden and nature, sports, fitness, cooking and DIY. BLV-books are almost exclusively original editions, licenses are sold in all European countries, the United States and in countries of the Asian continent.
>>>>>>
Answer: [Germany]
------
Question: Who was the quarterback selected two spots after the All American from the 1998 Kentucky Wildcats in the 1999 NFL draft?
Evidence: The 1998 Kentucky Wildcats football team represented the University of Kentucky in the 1998 NCAA Division I-A football season. Quarterback Tim Couch was the first pick overall in the 1999 NFL Draft.
>>>>>>
Answer: The evidence does not provide information about the quarterback selected two spots after Tim Couch in the 1999 NFL draft. However, based on knowledge, the second overall pick was [Donovan McNabb].
------
Question: Who was the quarterback selected two spots after the All American from the 1998 Kentucky Wildcats in the 1999 NFL draft?
Evidence: The 1998 Kentucky Wildcats football team represented the University of Kentucky in the 1998 NCAA Division I-A football season. Quarterback Tim Couch was the first pick overall in the 1999 NFL Draft.
>>>>>>
The evidence does not provide information about the quarterback selected two spots after Tim Couch in the 1999 NFL draft. However, based on knowledge, the second overall pick was Donovan McNabb.
Answer: [Donovan McNabb].
------
Question: Who was the All American quarterback from the 1998 Kentucky Wildcats football team?
Evidence: The 1998 Kentucky Wildcats football team represented the University of Kentucky in the 1998 NCAA Division I-A football season. Quarterback Tim Couch was the first pick overall in the 1999 NFL Draft.
>>>>>>
Answer: [Tim Couch]
------
Question: %s
Evidence: %s
>>>>>>
"""

LLM_rationale_true = """
Given the claim, with the relevant evidence: please provide a streamlined explanation associated with the claim and the evidence by using the contextual background and commonsense knowledge, to explicitly explain why the truth of the claim is reasoned as true.

Claim: %s
Evidence: %s
"""


LLM_rationale_false = """
Given the claim, with the relevant evidence: please provide a streamlined explanation associated with the claim and the evidence by using the contextual background and commonsense knowledge, to explicitly explain why the truth of the claim is reasoned as false.

Claim: %s
Evidence: %s
"""

LLM_decide = """
Given the claim [%s] and the following two claim rationales: (1) true: [%s]; (2) false: [%s], is this claim true or false?  Just output your prediction as "true" or "false".

"""

entity_program  = """
Find all the clear entities in the claim that can be find in the wikipedia.

Claim: In 1959, former Chilean boxer Alfredo Cornejo Cuevas (born June 6, 1933) won the gold medal in the welterweight division at the Pan American Games (held in Chicago, United States, from August 27 to September 7) in Chicago, United States, and the world amateur welterweight title in Mexico City.
>>>>>>
Entities: [Alfredo Cornejo Cuevas, Pan American Games, Chicago, United States, Mexico City]
------
Claim: The Footwork FA12, which was intended to start the season, finally debuted at the San Marino Grand Prix, a Formula One motor race held at Imola on 28 April 1991.
>>>>>>
Entities: [Footwork FA12, San Marino Grand Prix]
------
Claim: SkyHigh Mount Dandenong (formerly Mount Dandenong Observatory) is a restaurant located on top of Mount Dandenong, Victoria, Australia.
>>>>>>
Entities: [SkyHigh Mount Dandenong, Mount Dandenong]
------
Claim: Before the first Europeans arrived or copra companies leased it, Maupihaa was home to Inca's in ancient times.
>>>>>>
Entities: [Maupihaa]
------
Claim: Shulin, a 33.1288 km (12.7911 sq mi) land located in New Taipei City, China, a country in East Asia, has a total population of 183,946 in December 2018.
>>>>>>
Entities: [Shulin, New Taipei City, China]
------
Claim: Sumo wrestler Toyozakura Toshiaki committed match-fixing, ending his career in 2011 that started in 1989.
>>>>>>
Entities: [Toyozakura Toshiaki]
------
------
Claim: Adductor hiatus is associated with nine structures, seven of which enter and leave through hiatus.
>>>>>>
Entities: [Adductor hiatus]
------
Claim: Ifor Bowen Lloyd was educated at Winchester (an independent boarding school for boys in the British public school tradition) and Exeter College, Oxford where he was a member of the Library Committee of the Oxford Union Society, as well as, received a BA in Modern History in 1924.
>>>>>>
Entities: [Ifor Bowen Lloyd, Winchester, Exeter College, Oxford]
------
Claim: The song recorded by Fergie that was produced by Polow da Don and was followed by Life Goes On was M.I.L.F.$.
>>>>>>
Entities: [Fergie, Polow da Don]
------
Claim: Born December 30, 1974, William Frick was a dark horse candidate in the Maryland House of Delegates appointment process.
>>>>>>
Entities: [William Frick, Maryland House of Delegates]
------
Claim: The model of car Trevor Bayne drives was introduced for model year 2006. The Rookie of The Year in the 1997 CART season drives it in the NASCAR Sprint Cup.
>>>>>>
Entities: [Trevor Bayne, NASCAR Sprint Cup]
------
Claim: Party of Syrian Unity was established in the wake of a public statement that announced support for the establishment of a \"national home for the British people\" in Palestine.
>>>>>>
Entities: [Syrian Unity Party]
------
Claim: %s
>>>>>>
"""