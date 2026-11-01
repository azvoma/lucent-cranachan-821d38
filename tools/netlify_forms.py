#!/usr/bin/env python3
"""
Site email + Netlify Forms set-up (Nov 2026).  Safe to re-run.

- Every contact address -> hello@ukrugbyclubdirectory.co.uk (pages, structured data, blog template)
- Footer "Get Involved" column gains the email on every page
- Contact page gets a Netlify contact form ("contact")
- Claim and register forms move from unconfigured Formspree placeholders to Netlify Forms
  ("claim-listing", "register-club"), with a honeypot field against spam
- /thank-you.html (noindex) is shown after any form is sent
Netlify only picks forms up once Form detection is enabled in the Netlify UI
(Site configuration -> Forms -> Enable form detection) and the site is redeployed.
"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = 'hello@ukrugbyclubdirectory.co.uk'
OLD = ('contact@ukrugbyclubdirectory.co.uk', 'hello@anoziva.com')
HONEYPOT = ('<p class="nf-hp" hidden><label>Leave this empty: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>')


def rw(path, fn):
    s = open(path, encoding='utf-8', errors='surrogateescape').read()
    t = fn(s)
    if t != s:
        open(path, 'w', encoding='utf-8', errors='surrogateescape').write(t)
        return 1
    return 0


def emails(s):
    for o in OLD:
        s = s.replace(o, EMAIL)
    return s


def footer(s):
    if f'mailto:{EMAIL}">{EMAIL}</a></li>' in s:
        return s
    return re.sub(r'(<li><a href="((?:\.\./|/)?)contact-us\.html">Contact Us</a></li>)',
                  lambda m: m.group(1) + f'\n        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>', s, count=1)


CONTACT_FORM = f'''<!--nf-contact-->
    <div class="nf-card" id="contact-form">
      <h2 style="margin-bottom:.35rem">Send us a message</h2>
      <p style="color:var(--text-secondary);font-size:.92rem;margin-bottom:1.5rem">We reply within 1 working day. You can also email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <form name="contact" method="POST" action="/thank-you.html?form=contact" data-netlify="true" netlify-honeypot="bot-field" class="nf-form">
        <input type="hidden" name="form-name" value="contact">
        {HONEYPOT}
        <div class="nf-row">
          <p><label for="cf-name">Your name *</label><input id="cf-name" class="form-input" name="name" type="text" required autocomplete="name"></p>
          <p><label for="cf-email">Email address *</label><input id="cf-email" class="form-input" name="email" type="email" required autocomplete="email"></p>
        </div>
        <div class="nf-row">
          <p><label for="cf-topic">What is it about? *</label><select id="cf-topic" class="form-select" name="topic" required>
            <option value="">Choose one</option>
            <option>General enquiry</option>
            <option>Update or correct a club listing</option>
            <option>Add my club to the directory</option>
            <option>Remove a listing</option>
            <option>Advertising or partnership</option>
            <option>Report a problem with the website</option>
          </select></p>
          <p><label for="cf-club">Club or business name</label><input id="cf-club" class="form-input" name="club" type="text" autocomplete="organization"></p>
        </div>
        <p><label for="cf-message">Message *</label><textarea id="cf-message" class="form-input" name="message" rows="6" required></textarea></p>
        <p class="nf-note">We only use your details to reply to this message. See our <a href="privacy-policy.html">privacy policy</a>.</p>
        <p><button type="submit" class="btn btn-red btn-lg">Send message</button></p>
      </form>
    </div>
<!--/nf-contact-->
'''


def contact_page(s):
    s = re.sub(r'<!--nf-contact-->.*?<!--/nf-contact-->\n?', '', s, flags=re.S)
    return s.replace('<section class="sec">\n  <div class="con" style="max-width:680px;margin:0 auto">\n',
                     '<section class="sec">\n  <div class="con" style="max-width:680px;margin:0 auto">\n' + CONTACT_FORM, 1)


def netlify_form(s, form_id, name, success):
    m = re.search(rf'<form id="{form_id}"[^>]*>', s)
    if not m:
        return s
    tag = (f'<form id="{form_id}" name="{name}" method="POST" action="{success}" data-netlify="true" '
           f'netlify-honeypot="bot-field"' + (' style="display:flex;flex-direction:column;gap:1.25rem"' if 'style=' in m.group(0) else '') + '>')
    body_start = m.end()
    s = s[:m.start()] + tag + s[body_start:]
    # Formspree-only fields
    s = re.sub(r'\s*<input type="hidden" name="_(?:subject|redirect)"[^>]*>', '', s)
    if f'name="form-name" value="{name}"' not in s:
        i = s.find(tag) + len(tag)
        s = s[:i] + f'\n          <input type="hidden" name="form-name" value="{name}">\n          {HONEYPOT}' + s[i:]
    return s


THANKS_MAIN = f'''<main id="main">
<section class="sec">
  <div class="con" style="max-width:640px;margin:0 auto;text-align:center;padding:3rem 0">
    <h1 style="margin-bottom:.75rem">Thank you</h1>
    <p id="ty-text" style="font-size:1.05rem;color:var(--text-secondary);line-height:1.7;margin-bottom:1.75rem">Your message has been sent. We reply within 1 working day.</p>
    <p style="font-size:.92rem;color:var(--text-secondary);margin-bottom:2rem">Anything else? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    <p><a href="index.html" class="btn btn-red">Back to the directory</a></p>
  </div>
</section>
<script>
(function(){{var f=new URLSearchParams(location.search).get('form');var t=document.getElementById('ty-text');
if(f==='claim')t.textContent='Your claim request has been sent. We will check you are an official of the club and be in touch within 1 working day.';
if(f==='register')t.textContent='Your club registration has been sent. We will review it and let you know when the listing is live.';}})();
</script>
</main>'''


def build_thanks():
    src = open(os.path.join(ROOT, 'contact-us.html'), encoding='utf-8').read()
    s = re.sub(r'<title>[^<]*</title>', '<title>Thank You | UK Rugby Club Directory</title>', src, count=1)
    s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex,follow">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="https://ukrugbyclubdirectory.co.uk/thank-you.html">', s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Thanks for getting in touch with UK Rugby Club Directory.">', s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', s, flags=re.S)
    s = re.sub(r'<main id="main">.*?</main>', lambda m: THANKS_MAIN, s, count=1, flags=re.S)
    p = os.path.join(ROOT, 'thank-you.html')
    old = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
    if s != old:
        open(p, 'w', encoding='utf-8').write(s)
        return 1
    return 0


PRIVACY_OLD = 'We collect information you voluntarily submit via our registration and contact forms, including name, email address and club details. We do not sell your data to third parties.'
PRIVACY_NEW = ('We collect information you voluntarily submit via our contact, club registration and claim forms, including name, '
               'email address and club details. Form submissions are processed and stored by our website host, Netlify, and are used '
               f'only to reply to you and to update the directory. We do not sell your data to third parties. You can contact us at '
               f'<a href="mailto:{EMAIL}">{EMAIL}</a>.')


def main():
    n = 0
    files = glob.glob(os.path.join(ROOT, '*.html')) + glob.glob(os.path.join(ROOT, 'club', '*.html'))
    for p in files:
        n += rw(p, lambda s: footer(emails(s)))
    for p in [os.path.join(ROOT, 'netlify', 'plugins', 'generate-blog', 'index.js')] + glob.glob(os.path.join(ROOT, 'content', 'blog', '*.md')) + glob.glob(os.path.join(ROOT, 'js', '*.js')):
        n += rw(p, lambda s: footer(emails(s)))
    n += rw(os.path.join(ROOT, 'contact-us.html'), contact_page)
    n += rw(os.path.join(ROOT, 'claim.html'), lambda s: netlify_form(s, 'claim-form', 'claim-listing', '/thank-you.html?form=claim'))
    n += rw(os.path.join(ROOT, 'register.html'), lambda s: netlify_form(s, 'register-form', 'register-club', '/thank-you.html?form=register'))
    n += rw(os.path.join(ROOT, 'privacy-policy.html'),
            lambda s: s.replace(PRIVACY_OLD, PRIVACY_NEW).replace('Last updated: January 2025.', 'Last updated: November 2026.'))
    n += build_thanks()
    print(f'{n} file(s) updated')


if __name__ == '__main__':
    main()
