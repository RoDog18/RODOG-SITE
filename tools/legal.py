# Legal and support pages for the RoDog Audio site. build.py turns each entry into <slug>.html at the site root.
# Body text is plain HTML. CONTACT is the one place the support address lives.
CONTACT = "rodogaudio@protonmail.com"
UPDATED = "2 November 2026"

PAGES = [
 dict(slug="licence", title="Licence agreement", nav="Licence", body=f"""
<p>This licence agreement is between you and RoDog Audio, an Australian business (the "Seller"). It applies to every
RoDog Audio plug-in, the RoDog Product Manager and anything else we let you download (the "Software"). By installing
or using the Software you agree to it.</p>

<h2>What you can do</h2>
<ul>
  <li>When you buy a licence, you can install and use the Software on up to <strong>3 computers</strong> that you own or
    mainly use. Your licence key or account controls this.</li>
  <li>You can use the Software to make music, sound and any other audio, for personal or commercial work. What you
    make with it is yours. You don't owe us anything for it.</li>
  <li>Free versions and demos can be used under the same terms, with any limits we state for them.</li>
</ul>

<h2>What you can't do</h2>
<ul>
  <li>Share, sell, rent, lend or give away your licence key, the installers or the plug-in files.</li>
  <li>Copy, decompile, reverse engineer or change the Software, or get around its licence checks, except where the law
    allows it no matter what this agreement says.</li>
  <li>Use the Software's sounds, presets or graphics to build a competing product.</li>
</ul>

<h2>Ownership</h2>
<p>We own the Software, its code, presets, graphics and names. You are buying a licence to use it, not the Software
itself.</p>

<h2>Transfers</h2>
<p>Licences can't be transferred to another person unless we agree in writing.</p>

<h2>Updates</h2>
<p>We may release updates that fix problems or add features. Updates within the same major version (for example 1.0 to
1.9) are free. A new major version may be a paid upgrade.</p>

<h2>Your rights under Australian law</h2>
<p>Our goods come with guarantees that cannot be excluded under the Australian Consumer Law. Nothing in this agreement
limits those rights or any other right you have that the law says can't be taken away.</p>

<h2>Limits</h2>
<p>To the extent the law allows, the Software is provided as it is, and we aren't responsible for lost data, lost work or
lost profit caused by using it. Back up your projects. Where the law lets us limit what we owe, our total liability is
limited to the price you paid for the licence, or to supplying or fixing the Software again.</p>

<h2>Ending the licence</h2>
<p>If you break this agreement, your licence ends and you must remove the Software. If you get a refund, the licence for
that purchase ends too.</p>

<h2>Law</h2>
<p>This agreement is governed by the law of New South Wales, Australia.</p>

<p>Questions? Email <strong>{CONTACT}</strong>.</p>
"""),

 dict(slug="privacy", title="Privacy policy", nav="Privacy", body=f"""
<p>RoDog Audio collects as little about you as it can. This page explains what we do collect, why, and who else sees
it.</p>

<h2>When you buy</h2>
<p>Our online store and checkout are run by <strong>Lemon Squeezy</strong>, which is the seller of record for our
products. Lemon Squeezy collects your name, email address, billing country, payment details and tax information to take
your payment, work out tax and send your receipt and licence key. Your card details go to Lemon Squeezy and its payment
processor, never to us. Lemon Squeezy shares your name, email, country, what you bought and your licence key with us
so we can support you. Lemon Squeezy's own privacy policy explains how they handle your data.</p>

<h2>When you use our software</h2>
<p>When the RoDog Product Manager installs or updates plug-ins, or a plug-in checks its licence, your computer sends
your licence key and a computer identifier so we can confirm the licence and count activations. We don't collect your
audio, your projects or what you do in your music software.</p>

<h2>When you visit this website</h2>
<p>This website doesn't use cookies, ads or tracking. The website is hosted on GitHub Pages and loads fonts from Google
Fonts, so those services see your IP address when you visit, as with any website.</p>

<h2>When you email us</h2>
<p>We keep your messages so we can help you and keep a record of support.</p>

<h2>What we do with it</h2>
<ul>
  <li>Deliver and support what you bought, and check licences.</li>
  <li>Email you about your purchases and important product updates.</li>
  <li>Send news or offers only if you've signed up for them. You can unsubscribe at any time.</li>
</ul>
<p>We never sell your personal information.</p>

<h2>Your choices</h2>
<p>You can ask us what we hold about you, ask us to correct it, or ask us to delete it, by emailing
<strong>{CONTACT}</strong>. If you live in the EU or UK you also have rights under the GDPR. We handle personal
information in line with the Australian Privacy Principles. If you're not happy with how we've handled your information,
you can contact the Office of the Australian Information Commissioner (oaic.gov.au).</p>

<p>Last updated {UPDATED}.</p>
"""),

 dict(slug="refunds", title="Refund policy", nav="Refunds", body=f"""
<p>We want you to be happy with every RoDog Audio plug-in.</p>

<h2>If it doesn't work on your computer</h2>
<p>If a plug-in won't install or run properly on a system we list as supported, email <strong>{CONTACT}</strong> within
<strong>14 days</strong> of buying it. We'll try to fix it with you first. If we can't, we'll give you a full refund.</p>

<h2>Changed your mind</h2>
<p>Because plug-ins are digital downloads, we don't normally refund a change of mind. If you bought the wrong plug-in by
mistake and haven't used it, email us within 14 days and we'll sort it out.</p>

<h2>How refunds work</h2>
<p>Refunds go back to the card or account you paid with, through our store, Lemon Squeezy. When a purchase is refunded,
its licence key stops working.</p>

<h2>Your rights under Australian law</h2>
<p>Our goods come with guarantees that cannot be excluded under the Australian Consumer Law. If a product has a major
failure, you're entitled to a refund or replacement. Nothing in this policy limits those rights.</p>

<p>Last updated {UPDATED}.</p>
"""),

 dict(slug="support", title="Support", nav="Support", body=f"""
<p>Need a hand with a RoDog Audio plug-in? Email <strong>{CONTACT}</strong> and include:</p>
<ul>
  <li>the plug-in and its version</li>
  <li>your computer (Mac or Windows, and the system version)</li>
  <li>your music software (DAW) and its version</li>
  <li>what happened, and what you expected to happen</li>
</ul>
<p>We usually reply within two working days (Sydney time).</p>

<h2>Lost your licence key or download?</h2>
<p>Your licence keys and downloads are in the receipt email from our store, Lemon Squeezy. You can also find them any
time on Lemon Squeezy's "My Orders" page, using the email you bought with.</p>

<h2>Policies</h2>
<p><a href="licence.html">Licence agreement</a> · <a href="privacy.html">Privacy policy</a> ·
<a href="refunds.html">Refund policy</a></p>
"""),
]
