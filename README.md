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

