#!/usr/bin/env python3
"""Regenerate the per-paper pages under papers/ from a single source of truth.

Usage:  python3 tools/gen_papers.py

Add a new paper by appending a tuple to PAPERS, then re-run. The slug becomes
the filename (papers/<slug>.html), so link to it as papers/<slug>.html.
"""

import html
import pathlib
import re

OUT = pathlib.Path(__file__).resolve().parent.parent / "papers"

# slug, title, authors, journal, arxiv, doi (may be ""), inspire id (may be ""), blurb
PAPERS = [
    (
        'paper-2607-05335',
        'Galactic Center Neutrinos from Cosmic Ray–Dark Matter Interactions',
        'J. Terol Calvo, P. de la Torre Luque, M. Mukhopadhyay, C. Cappiello and G. Herrera',
        'Submitted to Physical Review D, under review (2026)',
        '2607.05335',
        '',
        '',
        'If dark matter interacts with ordinary matter at all, then the cosmic rays propagating through the Galaxy are '
        'already colliding with it. Above a certain momentum transfer the proton breaks apart, producing a shower of '
        'Standard Model particles, neutrinos among them. Here we compute that neutrino flux from the Galactic Centre for '
        'the first time with a realistic treatment of the collision and the hadronisation, then recast public ANTARES '
        'data to test for it. No signal is found, which gives some of the strongest limits available on dark matter '
        'between a keV and a GeV.',
    ),
    (
        'paper-2603-19109',
        'Searching for dark matter X-ray lines from the Large Magellanic Cloud with eROSITA',
        'J. Terol Calvo, M. Taoso, A. Caputo, M. Negro and M. Regis',
        'JCAP <strong>09</strong> (2026) 084',
        '2603.19109',
        '10.1088/1475-7516/2026/09/084',
        '',
        'A search for monochromatic X-ray emission from dark matter decay in the halo of the Large Magellanic Cloud, '
        'using eROSITA-DE DR1 data over 1–9 keV. We consider two candidates, sterile neutrinos and axion-like particles. '
        'No evidence for a dark matter line is found, so we set lower limits on the dark matter lifetime, constraining '
        'the active–sterile mixing angle and the ALP–photon coupling for masses of 2–18 keV. The bounds are strongest '
        'below 5 keV.',
    ),
    (
        'paper-2933174',
        'The Highest-Energy Neutrino Event Constrains Dark Matter–Neutrino Interactions',
        'T. Bertólez-Martínez, G. Herrera, P. Martínez-Miravé and J. Terol Calvo',
        'Phys. Rev. D <strong>113</strong> (2026) 103052',
        '2506.08993',
        '10.1103/ds8v-lvmw',
        '2933174',
        'KM3NeT detected a neutrino of about 100 PeV, by some margin the most energetic ever observed. It crossed a great '
        'deal of dark matter on its way to us, and if the two interact it should have been scattered or absorbed en '
        'route, so its arrival is itself informative. We work out what it implies, and the resulting constraint is '
        'competitive with far more elaborate searches.',
    ),
    (
        'paper-2860389',
        'Searching for axion-like particles with SPHEREx',
        'M. Regis, M. Taoso and J. Terol Calvo',
        'JCAP <strong>05</strong> (2025) 008',
        '2412.12286',
        '10.1088/1475-7516/2025/05/008',
        '2860389',
        'The same decay line, at longer wavelengths. SPHEREx is surveying the whole sky in the near infrared, the right '
        'band for axion-like particles of around an eV. We assess how deep the survey can go and which targets are most '
        'promising.',
    ),
    (
        'paper-2855514',
        'Searches for signatures of ultralight axion dark matter in polarimetry data of the European Pulsar Timing Array',
        'N. K. Porayko, P. Usynina, J. Terol-Calvo <em>et al.</em> (EPTA Collaboration)',
        'Phys. Rev. D <strong>111</strong> (2025) 062005',
        '2412.02232',
        '10.1103/PhysRevD.111.062005',
        '2855514',
        'If dark matter is light enough it behaves less like a collection of particles than like a wave filling the '
        'galaxy. A polarised beam crossing that wave would have its polarisation angle oscillate slowly, at a frequency '
        'set by the dark matter mass. Pulsars provide highly polarised beams and decades of monitoring, so we searched '
        'for that oscillation in European Pulsar Timing Array data.',
    ),
    (
        'paper-2211-01729',
        'A seesaw model for large neutrino masses in concordance with cosmology',
        'M. Escudero, T. Schwetz and J. Terol-Calvo',
        'JHEP <strong>02</strong> (2023) 142; Addendum: JHEP <strong>06</strong> (2024) 119',
        '2211.01729',
        '10.1007/JHEP02(2023)142',
        '',
        'There is a long-standing tension in neutrino physics: cosmology requires the neutrino masses to sum to a very '
        'small value, while laboratory experiments such as KATRIN are designed to look for masses that cosmology appears '
        'to have excluded. We construct a model in which both can hold, with neutrinos heavy today but effectively '
        'massless in the early universe. The addendum adds a mechanism that opens the parameter space further.',
    ),
    (
        'paper-2201-07805',
        'New physics searches at kaon and hyperon factories',
        'E. Goudzovski, D. Redigolo, K. Tobioka, J. Zupan <em>et al.</em> (incl. J. Terol-Calvo)',
        'Rept. Prog. Phys. <strong>86</strong> (2023) 016201',
        '2201.07805',
        '10.1088/1361-6633/ac9cee',
        '',
        'A large community review of new physics searches at kaon and hyperon facilities, much of it concerned with dark '
        'sectors. My contribution was the dark photon results, derived from the supernova cooling analysis of our earlier '
        'paper.',
    ),
    (
        'paper-2201-03422',
        'Searching for dark-matter waves with PPTA and QUIJOTE pulsar polarimetry',
        'A. Castillo, J. Martín-Camalich, J. Terol-Calvo, D. Blas, A. Caputo, R. T. Génova-Santos, L. Sberna, M. Peel and J. A. Rubiño-Martín',
        'JCAP <strong>06</strong> (2022) 014',
        '2201.03422',
        '10.1088/1475-7516/2022/06/014',
        '',
        'The first application of the pulsar polarimetry method, combining Parkes timing data with QUIJOTE observations '
        'from Tenerife. The later EPTA analysis grew out of this work.',
    ),
    (
        'paper-2104-03705',
        '(g−2)<sub>e,μ</sub> in an extended inverse type-III seesaw model',
        'P. Escribano, J. Terol-Calvo and A. Vicente',
        'Phys. Rev. D <strong>103</strong> (2021) 115018',
        '2104.03705',
        '10.1103/PhysRevD.103.115018',
        '',
        'At the time both the electron and muon magnetic moments appeared to deviate from the Standard Model prediction, '
        'and in opposite directions. We asked whether a single model could account for both while also generating '
        'neutrino masses, and found that an extended inverse type-III seesaw largely can.',
    ),
    (
        'paper-2012-11632',
        'Supernova Constraints on Dark Flavored Sectors',
        'J. Martín-Camalich, J. Terol-Calvo, L. Tolos and R. Ziegler',
        'Phys. Rev. D <strong>103</strong> (2021) L121301 (Rapid Communication)',
        '2012.11632',
        '10.1103/PhysRevD.103.L121301',
        '',
        'A core-collapse supernova is an exceptionally powerful particle physics laboratory. A new light particle would '
        'be produced in the hot core and escape, cooling the star faster than observations allow. We applied that '
        'argument for the first time to dark sectors coupled to quark flavour, and the resulting bounds exceed the '
        'terrestrial ones over a wide range.',
    ),
    (
        'paper-1912-09131',
        'High-energy constraints from low-energy neutrino nonstandard interactions',
        'J. Terol-Calvo, M. Tórtola and A. Vicente',
        'Phys. Rev. D <strong>101</strong> (2020) 095010',
        '1912.09131',
        '10.1103/PhysRevD.101.095010',
        '',
        'My first paper. Neutrino experiments operate at very low energies, so it is tempting to assume they say little '
        'about physics at the TeV scale. Carried through carefully in effective field theory, it turns out they do: in '
        'some directions the limits are as strong as those from colliders.',
    ),
]

# slug -> (image filename in assets/img/figures/, caption)
FIGURES = {
    "paper-2607-05335": ("paper-2607-05335.png",
        "Exclusion on the elastic dark matter\u2013proton cross section against dark matter mass, for mediator "
        "masses of 100 MeV (orange) and 5 GeV (red). Solid curves are the limits recast from ANTARES; dotted and "
        "dashed show the reach of IceCube, IceCube-Gen2 and KM3NeT. Shaded regions are existing constraints."),
    "paper-2603-19109": ("paper-2603-19109.png",
        "Upper limit on the axion\u2013photon coupling from the Large Magellanic Cloud using eROSITA-DE DR1 "
        "(purple), over the previously excluded region (grey)."),
    "paper-2933174": ("paper-2933174.png",
        "Constraint on the dark matter\u2013neutrino cross section per unit dark matter mass as a function of "
        "neutrino energy, set by KM3-230213A, compared with limits from other sources and with cosmology."),
    "paper-2855514": ("paper-2855514.png",
        "Upper limits on the axion\u2013photon coupling against boson mass from EPTA pulsar polarimetry, for the "
        "frequentist and Bayesian analyses, shown against CAST, SN1987A, Planck, BICEP-Keck, MOJAVE and the "
        "earlier PPTA\u2013QUIJOTE result."),
    "paper-2860389": ("paper-2860389.png",
        "Projected SPHEREx sensitivity to the axion\u2013photon coupling: deep-field observations of the Milky Way "
        "halo and the LMC, and an all-sky stack of dwarf spheroidals, against existing bounds."),
    "paper-2211-01729": ("paper-2211-01729.png",
        "The mechanism that hides the neutrino mass from cosmology. Above, neutrinos annihilate into the mediator "
        "X, which decays into massless dark states. Below, the resulting number densities: the active neutrino "
        "density is depleted between BBN and recombination, relaxing the cosmological mass bound."),
    "paper-2201-07805": ("paper-2201-07805.png",
        "Reach in the new-physics scale for the dimension-five massless dark photon operators. The SN1987A bars "
        "are the supernova cooling constraints I contributed, set against collider, BBN, stellar and kaon limits."),
    "paper-2201-03422": ("paper-2201-03422.png",
        "Axion dark matter behaves as a wave filling the galaxy. Polarised light leaving a pulsar (1) and arriving "
        "at a radio telescope (2) has its polarisation angle rotated by a time-dependent birefringence "
        "\u0394\u03c6(t). Illustration by \u00c8ve Barlier."),
    "paper-2104-03705": ("paper-2104-03705.png",
        "One of the W-boson loop diagrams contributing to the lepton anomalous magnetic moment in the extended "
        "inverse type-III seesaw, with the heavy neutral state N running in the loop."),
    "paper-2012-11632": ("paper-2012-11632.png",
        "Dark luminosity for a range of SN1987A simulations at about one second post-bounce, as a function of the "
        "branching fraction of \u039b \u2192 n X\u2070. The grey region is excluded by the neutrino luminosity "
        "bound."),
    "paper-1912-09131": ("paper-1912-09131.png",
        "Scale of new physics probed by each SMEFT operator: the bounds from neutrino non-standard interactions "
        "(blue) set against those from all other sources (red)."),
}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{plain_title} — Jorge Terol Calvo</title>
<link rel="icon" href="../assets/img/favicon.png">
<link rel="stylesheet" href="../assets/css/style.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <a class="nav-home" href="../index.html">Jorge Terol Calvo</a>
    <a href="../index.html#research">Research</a>
    <a href="../publications.html" aria-current="page">Papers</a>
    <a href="../cv.html">CV</a>
    <a href="../index.html#contact">Contact</a>
  </div>
</nav>

<div class="shell">
<aside class="rail">
  <a class="rail-id" href="../index.html">
    <img class="rail-photo" src="../assets/img/profile-img.jpg" alt="">
    <span class="rail-name">Jorge Terol&nbsp;Calvo</span>
  </a>
  <p class="rail-role">Theoretical astroparticle physics<br>INFN Torino</p>
  <nav class="rail-nav">
    <a href="../index.html#research">Research</a>
    <a href="../publications.html" aria-current="page">Papers</a>
    <a href="../cv.html">CV</a>
    <a href="../index.html#contact">Contact</a>
  </nav>
  <div class="rail-links">
    <a href="mailto:jortecal@protonmail.com" title="Email" aria-label="Email"><svg class="rail-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="m3 6.5 9 6 9-6"/></svg></a>
    <a href="https://inspirehep.net/authors/1774081" title="INSPIRE" aria-label="INSPIRE"><svg class="rail-ico brand-inspire" viewBox="0 0 512 512" fill="currentColor" aria-hidden="true"><path d="M32 32v448h448V32Zm77.673 79.678a34.076 34.076 0 0 1 34.076 34.076a34.076 34.076 0 0 1-34.076 34.076a34.076 34.076 0 0 1-34.076-34.076a34.076 34.076 0 0 1 34.076-34.076m76.17 9.02l64.173.16l116.23 187.258V120.698h59.132v280.626h-65.145l-112.25-185.413v185.413h-62.14ZM78.604 203.884h62.139v197.44H78.604z"/></svg></a>
    <a href="https://orcid.org/0000-0003-3117-5017" title="ORCID" aria-label="ORCID"><svg class="rail-ico brand-orcid" viewBox="0 0 512 512" fill="currentColor" aria-hidden="true"><path d="M336.62 194.538c-7.13-3.328-13.866-5.56-20.253-6.614c-6.365-1.095-16.574-1.612-30.71-1.612h-36.704v152.747h37.634c14.673 0 26.081-1.013 34.224-3.017s14.921-4.526 20.356-7.626a69.5 69.5 0 0 0 14.942-11.388c14.488-14.714 21.742-33.273 21.742-55.717c0-22.052-7.44-40.052-22.341-53.982c-5.498-5.166-11.822-9.444-18.89-12.793zM256 8C119.022 8 8 119.042 8 256s111.022 248 248 248s248-111.042 248-248S392.978 8 256 8m-82.336 357.513h-29.389V160.148h29.389zM158.95 138.696c-11.14 0-20.213-9.01-20.213-20.212c0-11.118 9.052-20.191 20.213-20.191c11.18 0 20.232 9.052 20.232 20.191a20.194 20.194 0 0 1-20.232 20.212m241.386 163.597c-5.29 12.545-12.834 23.581-22.65 33.088c-9.982 9.837-21.597 17.194-34.844 22.196c-7.75 3.017-14.839 5.063-21.307 6.117c-6.49 1.013-18.828 1.509-37.076 1.509h-64.956V160.148h69.233c27.962 0 50.034 4.154 66.32 12.545c16.265 8.37 29.181 20.728 38.792 36.972c9.61 16.265 14.425 34.018 14.425 53.196c.023 13.765-2.666 26.908-7.936 39.432z"/></svg></a>
    <a href="https://arxiv.org/a/terolcalvo_j_1" title="arXiv" aria-label="arXiv"><svg class="rail-ico brand-arxiv" viewBox="0 0 448 512" fill="currentColor" aria-hidden="true"><path d="M62.258 8.006a22.22 22.22 0 0 0-20.929 13.448c-3.404 8.169-.96 13.898 6.506 24.59c10.935 16.09 122.178 149.673 122.178 149.673l-24.619 23.038c-20.74 20.735-21.632 48.566-2.34 67.852l28.663 27.3l-79.976 98.235c-6.21 6.614-10.053 18.221-6.585 26.552a22.7 22.7 0 0 0 21.21 14.06a20.23 20.23 0 0 0 15.249-7.536l95.122-88.437L363.33 496.39a27.14 27.14 0 0 0 18.418 7.61a25.3 25.3 0 0 0 7.335-1.108a27.66 27.66 0 0 0 18.4-18.99a25.6 25.6 0 0 0-6.481-23.69L272.219 305.195l23.062-21.443c17.198-15.504 17.29-42.455.197-58.076l-25.257-24.228L357.417 98.46l.115-.133l.103-.14c7.793-10.123 11.52-17.92 7.502-27.806a36.17 36.17 0 0 0-23.647-18.37a24 24 0 0 0-3.166-.212l-.006.018a28.52 28.52 0 0 0-18.252 8.123l-.203.166l-.19.173L218.6 151.925L79.261 18.253S70.995 8.213 62.258 8.006m276.06 51.214q1.115.004 2.22.148a29.3 29.3 0 0 1 17.719 13.81c2.246 5.523 1.554 10.01-6.506 20.484L264.861 196.3l-40.882-39.22l100.68-91.304a21.77 21.77 0 0 1 13.66-6.536zM175.077 201.127L395.19 464.872c4.32 5.408 7.02 10.818 5.18 16.914a20.25 20.25 0 0 1-13.463 14.037a17.6 17.6 0 0 1-5.17.784a19.8 19.8 0 0 1-13.293-5.56l-220.15-209.694c-17.317-17.316-14.698-40.33 2.158-57.186z"/></svg></a>
    <a href="https://github.com/jorgetc16" title="GitHub" aria-label="GitHub"><svg class="rail-ico brand-github" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12c0 5.303 3.438 9.8 8.205 11.385c.6.113.82-.258.82-.577c0-.285-.01-1.04-.015-2.04c-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729c1.205.084 1.838 1.236 1.838 1.236c1.07 1.835 2.809 1.305 3.495.998c.108-.776.417-1.305.76-1.605c-2.665-.3-5.466-1.332-5.466-5.93c0-1.31.465-2.38 1.235-3.22c-.135-.303-.54-1.523.105-3.176c0 0 1.005-.322 3.3 1.23c.96-.267 1.98-.399 3-.405c1.02.006 2.04.138 3 .405c2.28-1.552 3.285-1.23 3.285-1.23c.645 1.653.24 2.873.12 3.176c.765.84 1.23 1.91 1.23 3.22c0 4.61-2.805 5.625-5.475 5.92c.42.36.81 1.096.81 2.22c0 1.606-.015 2.896-.015 3.286c0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg></a>
  </div>
</aside>

<main class="wrap">
  <section class="intro">
    <h1 style="font-size:1.45rem; line-height:1.3; margin:0 0 0.75rem">{title}</h1>
    <p class="pub-meta" style="font-size:0.95rem">{authors}</p>
    <p class="pub-meta" style="font-size:0.95rem">{journal}</p>
    <p style="margin-top:1.1rem">{links}</p>
  </section>

  <section>
    <h2>What it is about</h2>
    <p>{blurb}</p>
{figure}    <p style="margin-top:1.75rem"><a href="../publications.html">&larr; All papers</a></p>
  </section>
</main>
</div>

<footer class="site-footer">
  <div class="wrap">Last updated September 2026.</div>
</footer>

<button id="theme-toggle" class="theme-toggle" aria-label="Toggle dark mode" title="Toggle dark mode">🌓</button>
<script src="../assets/js/script.js"></script>
</body>
</html>
"""


def figure_block(slug: str) -> str:
    """The main-result figure for this paper, or nothing if none is set."""
    entry = FIGURES.get(slug)
    if not entry:
        return ""
    fn, caption = entry
    return (
        '    <figure class="figure-block">\n'
        f'      <img src="../assets/img/figures/{fn}" alt="{plain(caption)}">\n'
        f'      <figcaption>{caption}</figcaption>\n'
        '    </figure>\n\n'
    )


def plain(text: str) -> str:
    """Strip inline tags and escape entities, for use inside <title>."""
    return html.escape(re.sub(r"<[^>]+>", "", text))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for slug, title, authors, journal, arxiv, doi, inspire, blurb in PAPERS:
        links = [f'<a href="https://arxiv.org/abs/{arxiv}">arXiv:{arxiv}</a>']
        if doi:
            links.append(f'<a href="https://doi.org/{doi}">Journal version</a>')
        if inspire:
            links.append(f'<a href="https://inspirehep.net/literature/{inspire}">INSPIRE</a>')

        (OUT / f"{slug}.html").write_text(
            TEMPLATE.format(
                figure=figure_block(slug),
                plain_title=plain(title),
                title=title,
                authors=authors,
                journal=journal,
                links=" · ".join(links),
                blurb=blurb,
            ),
            encoding="utf-8",
        )
        print("wrote", slug)


if __name__ == "__main__":
    main()
