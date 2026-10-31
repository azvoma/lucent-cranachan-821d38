#!/usr/bin/env python3
"""
Remove league-level claims from club descriptions that contradict England Rugby
(checked 31 Oct 2026 against tools/er-teams.csv).  The real league now shows in the
key-facts strip from data, so the copy no longer names a level.  Each description
is reused in the club's About text, meta tags and club cards on other pages, so
the replacement runs across every live HTML page.  Safe to re-run.
"""
import glob, html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = {
 'Gateshead-based club competing in the National Leagues with a passionate fanbase along the Tyne.':
 'Gateshead-based club with a passionate fanbase along the Tyne.',
 'Berkshire new town club with a growing membership and competitive rugby in London and county leagues.':
 'Berkshire new town club with a growing membership and competitive league rugby.',
 'Essex market town club with strong competition in the London and county leagues.':
 'Essex market town club with competitive league rugby and a strong local following.',
 'South Devon fishing port club with a loyal community following and competitive rugby in county leagues.':
 'South Devon fishing port club with a loyal community following and competitive league rugby.',
 'North East Surrey club near Sandhurst with a large membership and competitive National League rugby.':
 'North East Surrey club near Sandhurst with a large membership and competitive league rugby.',
 'Border city club competing in the National Leagues with a strong membership across Cumbria.':
 'Border city club with a strong membership across Cumbria.',
 'Oxfordshire club competing in the National Leagues with excellent facilities in the Chiltern Hills.':
 'Oxfordshire club with excellent facilities in the Chiltern Hills.',
 'Spen Valley club competing in Yorkshire and national leagues from their Moorend ground.':
 'Spen Valley club playing league rugby from their Moorend ground.',
 'West Midlands National League club with a strong tradition at Oak Farm Road.':
 'West Midlands club with a strong tradition at Oak Farm Road.',
 'West Surrey market town club competing in the London and county leagues with a welcoming culture.':
 'West Surrey market town club with competitive league rugby and a welcoming culture.',
 'County Durham port town club competing in the National Leagues with strong local support.':
 'County Durham port town club with strong local support.',
 'South Cumbrian club based at Mintsfeet with competitive National League rugby and strong community ties.':
 'South Cumbrian club based at Mintsfeet with competitive league rugby and strong community ties.',
 'Thames Valley club with a large membership and competitive rugby in the London and Home Counties leagues.':
 'Thames Valley club with a large membership and competitive league rugby.',
 'North Wiltshire market town club with a welcoming ethos and competitive rugby in county leagues.':
 'North Wiltshire market town club with a welcoming ethos and competitive league rugby.',
 'South East London club with a proud former pupils tradition and competitive National League rugby.':
 'South East London club with a proud former pupils tradition and competitive league rugby.',
 'West Yorkshire market town club competing in county leagues from their Moor Lane ground.':
 'West Yorkshire market town club playing league rugby from their Moor Lane ground.',
 'South Essex club with a long history competing in London and Essex county leagues.':
 'South Essex club with a long history of league rugby.',
 'Kent market town club competing in the London and county leagues from their Knole Park ground.':
 'Kent market town club playing league rugby from their Knole Park ground.',
 'Wearside club competing in the National Leagues with strong local support in the North East.':
 'Wearside club with strong local support in the North East.',
 'South Hampshire club competing in the National Leagues with a strong playing history.':
 'South Hampshire club with a strong playing history.',
 'Kent spa town club competing in the National Leagues with a large and active membership.':
 'Kent spa town club with a large and active membership.',
 'Lancaster-based club competing in the National Leagues with excellent facilities at Powderhouse Lane.':
 'Lancaster-based club with excellent facilities at Powderhouse Lane.',
 'Nottinghamshire club competing in the National Leagues with strong community connections.':
 'Nottinghamshire club with strong community connections.',
 'historic Hartlepool club that once competed in the Premiership, now rebuilding from the National Leagues.':
 'historic Hartlepool club that once competed in the Premiership.',
 'Cheshire-based club competing in the National Leagues with excellent facilities at Pownall Park.':
 'Cheshire-based club with excellent facilities at Pownall Park.',
}


def variants(t):
    # raw, html-escaped, and without the final full stop (meta descriptions sometimes trim it)
    out = {t, html.escape(t, quote=False), html.escape(t)}
    return out


def main():
    pages = glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'club', '*.html')) \
        + [os.path.join(ROOT, 'js', 'clubs-index.json')]
    changed = hits = 0
    for p in pages:
        s = open(p, encoding='utf-8', errors='surrogateescape').read()
        o = s
        for old, new in FIX.items():
            for a, b in ((old, new), (old[0].upper() + old[1:], new[0].upper() + new[1:]),
                         (old.rstrip('.'), new.rstrip('.'))):
                for va in variants(a):
                    if va in s:
                        hits += s.count(va)
                        vb = html.escape(b, quote=False) if va != a else b
                        s = s.replace(va, vb)
        # cards elsewhere show the description cut short with an ellipsis
        def card(m):
            body = html.unescape(m.group(2))
            stem = body.rstrip('…').rstrip()
            if not body.endswith('…') or len(stem) < 25:
                return m.group(0)
            for old, new in FIX.items():
                for a, b in ((old, new), (old[0].upper() + old[1:], new[0].upper() + new[1:])):
                    if a.startswith(stem):
                        nt = b if len(b) <= len(stem) + 1 else b[:len(stem)].rstrip() + '…'
                        return m.group(1) + html.escape(nt, quote=False) + m.group(3)
            return m.group(0)
        s2 = re.sub(r'(<p class="club-desc">)([^<]*)(</p>)', card, s)
        if s2 != s:
            hits += 1; s = s2
        if s != o:
            open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s); changed += 1
    print(f'{hits} replacements on {changed} files')


if __name__ == '__main__':
    main()
