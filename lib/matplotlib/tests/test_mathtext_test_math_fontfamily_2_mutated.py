from __future__ import annotations
import io
from pathlib import Path
import platform
import re
from xml.etree import ElementTree as ET
from typing import Any
import numpy as np
from packaging.version import parse as parse_version
import pyparsing
import pytest
import matplotlib as mpl
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import matplotlib.pyplot as plt
from matplotlib import mathtext, _mathtext
pyparsing_version = parse_version(pyparsing.__version__)
math_tests = ['$a+b+\\dot s+\\dot{s}+\\ldots$', '$x\\hspace{-0.2}\\doteq\\hspace{-0.2}y$', '\\$100.00 $\\alpha \\_$', '$\\frac{\\$100.00}{y}$', '$x   y$', '$x+y\\ x=y\\ x<y\\ x:y\\ x,y\\ x@y$', '$100\\%y\\ x*y\\ x/y x\\$y$', '$x\\leftarrow y\\ x\\forall y\\ x-y$', '$x \\sf x \\bf x {\\cal X} \\rm x$', '$x\\ x\\,x\\;x\\quad x\\qquad x\\!x\\hspace{ 0.5 }y$', '$\\{ \\rm braces \\}$', '$\\left[\\left\\lfloor\\frac{5}{\\frac{\\left(3\\right)}{4}} y\\right)\\right]$', '$\\left(x\\right)$', '$\\sin(x)$', '$x_2$', '$x^2$', '$x^2_y$', '$x_y^2$', '$\\sum _{\\genfrac{}{}{0}{}{0\\leq i\\leq m}{0<j<n}}f\\left(i,j\\right)\\mathcal{R}\\prod_{i=\\alpha_{i+1}}^\\infty a_i \\sin(2 \\pi f x_i)\\sqrt[2]{\\prod^\\frac{x}{2\\pi^2}_\\infty}$', '$x = \\frac{x+\\frac{5}{2}}{\\frac{y+3}{8}}$', '$dz/dt = \\gamma x^2 + {\\rm sin}(2\\pi y+\\phi)$', 'Foo: $\\alpha_{i+1}^j = {\\rm sin}(2\\pi f_j t_i) e^{-5 t_i/\\tau}$', None, 'Variable $i$ is good', '$\\Delta_i^j$', '$\\Delta^j_{i+1}$', '$\\ddot{o}\\acute{e}\\grave{e}\\hat{O}\\breve{\\imath}\\tilde{n}\\vec{q}$', '$\\arccos((x^i))$', '$\\gamma = \\frac{x=\\frac{6}{8}}{y} \\delta$', '$\\limsup_{x\\to\\infty}$', None, "$f'\\quad f'''(x)\\quad ''/\\mathrm{yr}$", '$\\frac{x_2888}{y}$', '$\\sqrt[3]{\\frac{X_2}{Y}}=5$', None, '$\\sqrt[3]{x}=5$', '$\\frac{X}{\\frac{X}{Y}}$', '$W^{3\\beta}_{\\delta_1 \\rho_1 \\sigma_2} = U^{3\\beta}_{\\delta_1 \\rho_1} + \\frac{1}{8 \\pi 2} \\int^{\\alpha_2}_{\\alpha_2} d \\alpha^\\prime_2 \\left[\\frac{ U^{2\\beta}_{\\delta_1 \\rho_1} - \\alpha^\\prime_2U^{1\\beta}_{\\rho_1 \\sigma_2} }{U^{0\\beta}_{\\rho_1 \\sigma_2}}\\right]$', '$\\mathcal{H} = \\int d \\tau \\left(\\epsilon E^2 + \\mu H^2\\right)$', '$\\widehat{abc}\\widetilde{def}$', '$\\Gamma \\Delta \\Theta \\Lambda \\Xi \\Pi \\Sigma \\Upsilon \\Phi \\Psi \\Omega$', '$\\alpha \\beta \\gamma \\delta \\epsilon \\zeta \\eta \\theta \\iota \\lambda \\mu \\nu \\xi \\pi \\kappa \\rho \\sigma \\tau \\upsilon \\phi \\chi \\psi$', '${x}^{2}{y}^{2}$', '${}_{2}F_{3}$', '$\\frac{x+{y}^{2}}{k+1}$', '$x+{y}^{\\frac{2}{k+1}}$', '$\\frac{a}{b/2}$', '${a}_{0}+\\frac{1}{{a}_{1}+\\frac{1}{{a}_{2}+\\frac{1}{{a}_{3}+\\frac{1}{{a}_{4}}}}}$', '${a}_{0}+\\frac{1}{{a}_{1}+\\frac{1}{{a}_{2}+\\frac{1}{{a}_{3}+\\frac{1}{{a}_{4}}}}}$', '$\\binom{n}{k/2}$', '$\\binom{p}{2}{x}^{2}{y}^{p-2}-\\frac{1}{1-x}\\frac{1}{1-{x}^{2}}$', '${x}^{2y}$', '$\\sum _{i=1}^{p}\\sum _{j=1}^{q}\\sum _{k=1}^{r}{a}_{ij}{b}_{jk}{c}_{ki}$', '$\\sqrt{1+\\sqrt{1+\\sqrt{1+\\sqrt{1+\\sqrt{1+\\sqrt{1+\\sqrt{1+x}}}}}}}$', '$\\left(\\frac{{\\partial }^{2}}{\\partial {x}^{2}}+\\frac{{\\partial }^{2}}{\\partial {y}^{2}}\\right){|\\varphi \\left(x+iy\\right)|}^{2}=0$', '${2}^{{2}^{{2}^{x}}}$', '${\\int }_{1}^{x}\\frac{\\mathrm{dt}}{t}$', '$\\int {\\int }_{D}\\mathrm{dx} \\mathrm{dy}$', '${y}_{{x}^{2}}$', '${y}_{{x}_{2}}$', '${x}_{92}^{31415}+\\pi $', '${x}_{{y}_{b}^{a}}^{{z}_{c}^{d}}$', '${y}_{3}^{\\prime \\prime \\prime }$', '$\\left( \\xi \\left( 1 - \\xi \\right) \\right)$', '$\\left(2 \\, a=b\\right)$', '$? ! &$', None, None, '$\\left\\Vert \\frac{a}{b} \\right\\Vert \\left\\vert \\frac{a}{b} \\right\\vert \\left\\| \\frac{a}{b}\\right\\| \\left| \\frac{a}{b} \\right| \\Vert a \\Vert \\vert b \\vert \\| a \\| | b |$', '$\\mathring{A}  \\AA$', '$M \\, M \\thinspace M \\/ M \\> M \\: M \\; M \\ M \\enspace M \\quad M \\qquad M \\! M$', '$\\Cap$ $\\Cup$ $\\leftharpoonup$ $\\barwedge$ $\\rightharpoonup$', '$\\hspace{-0.2}\\dotplus\\hspace{-0.2}$ $\\hspace{-0.2}\\doteq\\hspace{-0.2}$ $\\hspace{-0.2}\\doteqdot\\hspace{-0.2}$ $\\ddots$', '$xyz^kx_kx^py^{p-2} d_i^jb_jc_kd x^j_i E^0 E^0_u$', '${xyz}^k{x}_{k}{x}^{p}{y}^{p-2} {d}_{i}^{j}{b}_{j}{c}_{k}{d} {x}^{j}_{i}{E}^{0}{E}^0_u$', '${\\int}_x^x x\\oint_x^x x\\int_{X}^{X}x\\int_x x \\int^x x \\int_{x} x\\int^{x}{\\int}_{x} x{\\int}^{x}_{x}x$', 'testing$^{123}$', None, '$6-2$; $-2$; $ -2$; ${-2}$; ${  -2}$; $20^{+3}_{-2}$', '$\\overline{\\omega}^x \\frac{1}{2}_0^x$', '$,$ $.$ $1{,}234{, }567{ , }890$ and $1,234,567,890$', '$\\left(X\\right)_{a}^{b}$', '$\\dfrac{\\$100.00}{y}$', '$a=-b-c$']
svgastext_math_tests = ['$-$-']
lightweight_math_tests = ['$\\sqrt[ab]{123}$', '$x \\overset{f}{\\rightarrow} \\overset{f}{x} \\underset{xx}{ff} \\overset{xx}{ff} \\underset{f}{x} \\underset{f}{\\leftarrow} x$', '$\\sum x\\quad\\sum^nx\\quad\\sum_nx\\quad\\sum_n^nx\\quad\\prod x\\quad\\prod^nx\\quad\\prod_nx\\quad\\prod_n^nx$', '$1.$ $2.$ $19680801.$ $a.$ $b.$ $mpl.$', '$\\text{text}_{\\text{sub}}^{\\text{sup}} + \\text{\\$foo\\$} + \\frac{\\text{num}}{\\mathbf{\\text{den}}}\\text{with space, curly brackets \\{\\}, and dash -}$', '$\\boldsymbol{abcde} \\boldsymbol{+} \\boldsymbol{\\Gamma + \\Omega} \\boldsymbol{01234} \\boldsymbol{\\alpha * \\beta}$', '$\\left\\lbrace\\frac{\\left\\lbrack A^b_c\\right\\rbrace}{\\left\\leftbrace D^e_f \\right\\rbrack}\\right\\rightbrace\\ \\left\\leftparen\\max_{x} \\left\\lgroup \\frac{A}{B}\\right\\rgroup \\right\\rightparen$', '$\\left( a\\middle. b \\right)$ $\\left( \\frac{a}{b} \\middle\\vert x_i \\in P^S \\right)$ $\\left[ 1 - \\middle| a\\middle| + \\left( x  - \\left\\lfloor \\dfrac{a}{b}\\right\\rfloor \\right)  \\right]$', '$\\sum_{\\substack{k = 1\\\\ k \\neq \\lfloor n/2\\rfloor}}^{n}P(i,j) \\sum_{\\substack{i \\neq 0\\\\ -1 \\leq i \\leq 3\\\\ 1 \\leq j \\leq 5}} F^i(x,y) \\sum_{\\substack{\\left \\lfloor \\frac{n}{2} \\right\\rfloor}} F(n)$']
digits = '0123456789'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppergreek = '\\Gamma \\Delta \\Theta \\Lambda \\Xi \\Pi \\Sigma \\Upsilon \\Phi \\Psi \\Omega'
lowergreek = '\\alpha \\beta \\gamma \\delta \\epsilon \\zeta \\eta \\theta \\iota \\lambda \\mu \\nu \\xi \\pi \\kappa \\rho \\sigma \\tau \\upsilon \\phi \\chi \\psi'
all = [digits, uppercase, lowercase, uppergreek, lowergreek]
font_test_specs: list[tuple[None | list[str], Any]] = [([], all), (['mathrm'], all), (['mathbf'], all), (['mathit'], all), (['mathtt'], [digits, uppercase, lowercase]), (None, 3), (None, 3), (None, 3), (['mathbb'], [digits, uppercase, lowercase, '\\Gamma \\Pi \\Sigma \\gamma \\pi']), (['mathrm', 'mathbb'], [digits, uppercase, lowercase, '\\Gamma \\Pi \\Sigma \\gamma \\pi']), (['mathbf', 'mathbb'], [digits, uppercase, lowercase, '\\Gamma \\Pi \\Sigma \\gamma \\pi']), (['mathcal'], [uppercase]), (['mathfrak'], [uppercase, lowercase]), (['mathbf', 'mathfrak'], [uppercase, lowercase]), (['mathscr'], [uppercase, lowercase]), (['mathsf'], [digits, uppercase, lowercase]), (['mathrm', 'mathsf'], [digits, uppercase, lowercase]), (['mathbf', 'mathsf'], [digits, uppercase, lowercase]), (['mathbfit'], all)]
font_tests: list[None | str] = []
for fonts, chars in font_test_specs:
    if fonts is None:
        font_tests.extend([None] * chars)
    else:
        wrapper = ''.join([' '.join(fonts), ' $', *('\\%s{' % font for font in fonts), '%s', *('}' for font in fonts), '$'])
        for font_set in chars:
            font_tests.append(wrapper % font_set)

@pytest.fixture
def baseline_images(request, fontset, index, text):
    if text is None:
        pytest.skip('test has been removed')
    return ['%s_%s_%02d' % (request.param, fontset, index)]

@image_comparison(baseline_images=['math_fontfamily_image.png'], savefig_kwarg={'dpi': 40})
def test_math_fontfamily_2_mutated():
    fig = plt.figure(figsize=(10, 3), frameon=False)
    fig.text(0.2, 0.7, '$This\\ text\\ should\\ have\\ one\\ font$', size=24, math_fontfamily='dejavusans')
    fig.text(0.2, 0.3, '$This\\ text\\ should\\ have\\ another$', size=24, math_fontfamily='stix')
# Mutation info: Added frameon = False (Call plt.figure)