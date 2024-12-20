from collections import defaultdict, Counter

if __name__ == "__main__":
    workspaceFolder = "C://Study/bar_ilan/year_2024A/NLP/ex_2"
    data_dir = f'{workspaceFolder}/part_b/data-pos'

    gold_standard_file = 'ass2-tagger-dev'
    output_file = 'ass2-tagger-dev-debug'

    tokens_predicted = 0
    tokens_wrong = 0
    unknown_token_wrong = 0
    token_to_wrong_count = Counter()
    token_to_wrong_pos = defaultdict(Counter)
    unknown_tokens = {'anti-recession', 'educations', 'easy-to-film', 'VA', 'Remic-related', 'anti-toxic', 'mirrors', 'Japanese-owned', 'typewriters', 'home-delivery', 'stat', 'JPI', 'woken', 'low-yielding', 'reactionary', 'program-related', 'parades', 
'mediation', 'high-leverage', 'homered', 'a.k.a.', 'depreciated', 'overpaying', 'anti-scientific', 'vitality', 'CENTRUST', 'photographers', 'taunting', 'multifaceted', 'latched', 'fish-processing', 'NGL', 'politico-plaintiffs', 'downshoot', 'bedside', 'meddle', 'novelty', 'computer-based', 'awash', 'exhilaration', 'brandished', '200-point', 'warranted', '1987-style', 'char-grilled', 'PARIS', 'carpeted', '2-1', 'belittle', 'CAC', 'infrared', 'OEL', 'NAHB', 'sales-loss', 'smoked', 'negligent', 'procession', 'U.N.-monitored', 'fluctuating', 'whistling', 'minisupercomputers', 'salve', 'pre-set', 'bluechip', 'SWAPO', '15-trader', 'dives', '600-point', 'watchful', 'un-advertising', 'apathy', 'photographed', 'manual', 'groove', 'forklifts', 'PerkinElmer', 'DiCara', 'home-delivered', 'ceremonies', 'civility', 'contradiction', '800-line', 'crewcut', 'unto', '88-points', '2-0', 'publishable', 'electro-optical', '3-for-3', '76-story', 'noncorrosive', 'pernicious', 'DeBat', 'dishwasher', 'powder', 'gauze', 'working-capital', 'millon', 'contests', 'ditto', 'bond-market', 'persuasiveness', 'tightness', 'booed', 'photofinishers', 'batted', 'steels', 'fixedrate', 'precipitating', 'revisited', 'DRG', 'advancement', 'leisure-oriented', 'SPRUCING', 'carnage', 'HOME-SALE', 'dispatches', 'well-connected', 'price-supporting', 'self-help', 'two-tone', 'underpinning', 'collectability', 'wholesale-store', 'hobbies', '20-a-share', 'reds', 'three-run', 'afield', '19-to-$21', 'prepurchase', 'un-advertisers', 'lunging', 'tunes', 'intergovernmental', 'initiatiors', 'pinched', 'slugger', 'rationality', 'jeopardized', 'lustily', 'trading-related', 'deplete', 'medalist', 'ARNOLD', '47%-controlled', 'registers', 'jaw', 'left-field', 'home-team', 'synchronize', 'rhetorical', 'suppressants', 'labor-shortage', 'intents', 'pessimist', 'wish-lists', 'manning', 'savior', 'union-bidder', 'hey', 'renting', 'herring', 'creations', 'conceivable', '6-4', 'non-accruing', 'urgings', 'localities', 'underwritings', 'bedlam', 'split-finger', 'resurging', 'whisper', 'fundamentalism', 'unlit', 'colorization', 'A-men', 'scarcity', 'confectionery', 'CLUBBING', 'signalling', 'power-hitter', 'marshal', 'pendulum', 'RTC-owned', 'relocations', 'twiggy-looking', 'spin-off', 'ADT', 'technologist', 'salted', 'groped', 'mischievous', 'second-year', 'wrung', 'plunking', 'IBEW', 'carefree', 'anti-defense', 'NRDC', 'precursory', 'BMA', 'margined', 'tiger', 'darkroom', '7-a-share', 'steepest', 'ribbies', 'open-bank', 'narrowness', 'good-humored', 'yelped', 'monochrome', 'straightening', 'rooters', 'apple-pie', 'airline-acquisition', 'swinging', 'BancOklahoma', 'archival', 'fundraisers', 'less-than-alarming', 'sell-order', '800-number', 'unanimity', 'federal-formula', 'mid', 'Marxist-dominated', 'rubric', 'DeMoulin', 'remnants', 'measurable', 'takeout', 'hatch', 'redress', 'RepublicBank', 'i860', 'glum', '1-for-17', 'snare', '7,500-share', 'SES', 'late-in-the-day', 'ex-hurler', 'right-to-work', 'photographer', '142-page', 'McClatchy', 'blinds', 'vented', '23-day', 'droughts', 'FRANKFURT', 'greenhouse-effect', 'homelessness', 'TCR', 'bifurcate', 'springs', 'pasted', 'brokered', '5-for-24', 'big-stock', 'goosey', 'pre-trading', 'scoring', 'McChicken', 'hammering', 'MRA', 'soulmates', 'biscuits', 'er', 'intercept', 'nonchlorinated', 'l987', 'NEATNESS', 'credence', 'microchip', 'enlargers', 'surfaces', 'foreign-trade', 'NPD', 'sighing', 'maligned', 'McVities', 'cotton-growing', 'leveraging', 'grocery-store', 'movie-production', 'stay-at-home', "O'Linn's", 'deflate', 'punched', 'septuagenarian', 'atrocities', '13-pound', 'ledger', 'hot-cold', 'ACCO', '941-105', 'lunchtime', 'rate-mortgages', 'sheep-like', 'low-', "ol'", 'leaps', 'WCRS/Boston', 'lifeline', 'Street-inspired', 'EUROPE', 'reining', 'anyhow', 'remiss', '24/32', 'bluest', 'combatants', 'parallel-computing', 'treads', '3-4-5', 'fish-export', 'winningest', 'cinematography', 'philosophically', 'six-hour', 'account-churning', '25-a-share', 'gaseous', '27-point', 'forlorn', 'paves', '150th', 'emblems', 'plutonium-powered', 'bonnets', 'balanced-budget', 'believable', 'lockstep', 'anti-pocketbook', 'compaction', 'HK', 'presuming', 'co-hero', 'inter-bank', '.9.82', 'quantum', 'anticompetitive', 'endorsers', 'conveyance', 'dispute-settlement', 'heckled', 'dealmakers', '21-9', 'fiddling', 'wish-list', 'mid-conversation', 'uniformed', '164.78-point', '49,000-plus', '9-8', 'anti-debt', 'wow', 'recovers', 'split-fingered', 'earth-moving', 'subtracting', 'tuning', 'temporary-help', '250-point', 'red-haired', 'suicidal', 'no-smoking'}
    with open(f'{data_dir}/{gold_standard_file}', 'r') as gold_standard:
        with open(f'{data_dir}/{output_file}', 'r') as debug:
            for debug_line, gold_standard_line in zip(debug, gold_standard):
                tag_pairs_debug_line, tag_pairs_gold_standard_line = debug_line.split(), gold_standard_line.split()
                for tag_pair_debug_line, tag_pairs_gold_standard_line in zip(tag_pairs_debug_line, tag_pairs_gold_standard_line):
                    tokens_predicted += 1
                    token_debug_line, pos_debug_line = tag_pair_debug_line.rsplit('/', 1)
                    token_gold_standard_line, pos_gold_standard_line = tag_pairs_gold_standard_line.rsplit('/', 1)
                    if pos_debug_line != pos_gold_standard_line:
                        tokens_wrong += 1
                        if token_debug_line != token_gold_standard_line:
                            raise Exception
                        if token_debug_line in unknown_tokens:
                            unknown_token_wrong += 1
                            token_to_wrong_count[f'UNKNOWN_{token_debug_line}'] += 1
                            token_to_wrong_pos[f'UNKNOWN_{token_debug_line}'][pos_gold_standard_line] += 1
                        else:
                            token_to_wrong_count[token_debug_line] += 1
                            token_to_wrong_pos[token_debug_line][pos_gold_standard_line] += 1
                        print(token_debug_line, pos_debug_line, pos_gold_standard_line)

            print(f'acc is {(tokens_predicted-tokens_wrong) / tokens_predicted}')
            # print(sorted(token_to_wrong.items(), key=lambda pair: pair[1]))
            print(token_to_wrong_count)
            # print(token_to_wrong_pos)
            print(f'{tokens_wrong} wrong tokens')
            print(f'{(unknown_token_wrong / tokens_wrong) * 100}% were unknown tokens')
