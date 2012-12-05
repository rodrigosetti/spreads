# Spreads

An automatic evaluation iterative calculator.

This is a simple but very effective and useful tool for making calculations.
You have a prompt where you can enter and evaluate expressions. Each time you
make an attribution, all previous attributions are updated and show to you.

To make things clear, please see a sample interaction below. All lines starting
with `>> ` are user inputs.

    >>  interest_rate = 0.07
    >>  down_payment = 6000
    >>  total = 28500
    >>  periods = 48
    >>  payment_per_period = ((total - down_payment) * (1 + interest_rate)) / periods
    501.5625
    >>  interest_rate = 0.055
    payment_per_period => 494.53125
    >>  down_payment = 5500
    payment_per_period => 505.520833333
    >>  ?
    total => 28500
    payment_per_period => 505.520833333
    interest_rate => 0.055
    down_payment => 5500
    periods => 48
    >>  ??
    total => 28500
    payment_per_period = ((total - down_payment) * (1 + interest_rate)) / periods => 505.520833333
    interest_rate => 0.055
    down_payment => 5500
    periods => 48
    >>  payment_per_period?
    ((total - down_payment) * (1 + interest_rate)) / periods => 505.520833333
    >>  payment_per_period * 1.08 + 100
    >>  645.9625

The six kinds of input one can enter are:

* Attributions (_e. g._ `x = 2*y`)
* Remove a value (_e. g._ `del x`)
* Free expressions (_e. g._ `sqrt(x) / 3`)
* Query about a value (_e. g._ `x?`)
* Query about all values: `?`
* Query about all values and their expressions: `??`

## Advanced Features

Since expressions are actually python expressions, one can use interesting
features such as lambdas:

    >>  tax_deduction = lambda x: x if x < 1023 else 0.73*x
    <function>
    >>  raw_income = 2100
    >>  after_tax_income = tax_deduction(raw_income)
    1533.0
    >>  raw_income = 800
    after_tax_income => 800
    >>  raw_income = 1055
    after_tax_income => 770.15
    >>  tax_deduction = lambda x: x if x < 1067 else 0.73*x
    after_tax_income => 1055

## Things to avoid

One may get strange behaviour if the expressions are self-referencing (even if
indirectly), such as:

    >>  x = 2
    >>  x = x**2
    x => 16
    16
    >>  y = 10
    x => 256

Also, when using non-deterministic and other kind of non-functional (_i. e._
collateral effects such as file reading or networking) expressions.

These are not prohibited expressions, but you are warned!

