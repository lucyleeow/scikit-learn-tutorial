import numpy as np
from matplotlib import pyplot as plt

# Set up figures look and feel
import style_figs

# %%
# Our data-generating process

def f(t):
    return 1.2 * t ** 2 + .1 * t ** 3 - .4 * t ** 5 - .5 * t ** 9

N_SAMPLES = 50

rng = np.random.RandomState(0)
x = 2 * rng.rand(N_SAMPLES) - 1

y = f(x) + .4 * rng.normal(size=N_SAMPLES)

plt.figure()
plt.scatter(x, y, s=20, color='k')

style_figs.no_axis()
plt.subplots_adjust(top=.96)
plt.xlim(-1.1, 1.1)
plt.ylim(-.74, 2.1)
plt.savefig('polynomial_overfit_0.svg', facecolor='none', edgecolor='none')

# %%
# Our model (polynomial regression)

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# %%
# Fit model with various complexity in the polynomial degree

plt.figure()
plt.scatter(x, y, s=20, color='k')

t = np.linspace(-1, 1, 100)

for d in (1, 2, 5, 9):
    model = make_pipeline(PolynomialFeatures(degree=d), LinearRegression())
    model.fit(x.reshape(-1, 1), y)
    plt.plot(t, model.predict(t.reshape(-1, 1)), label='Degree %d' % d)

    style_figs.no_axis()
    plt.legend(loc='upper center', borderaxespad=0, borderpad=0)
    plt.subplots_adjust(top=.96)
    plt.ylim(-.74, 2.1)

    plt.savefig('polynomial_overfit_%d.svg' % d, facecolor='none',
                edgecolor='none')

plt.plot(t, f(t), 'k--', label='Truth')

style_figs.no_axis()
plt.legend(loc='upper center', borderaxespad=0, borderpad=0)
plt.ylim(-.74, 2.1)
plt.subplots_adjust(top=.96)

plt.savefig('polynomial_overfit.svg', facecolor='none', edgecolor='none')

# %%
# A figure with the true model and the estimated one

plt.figure(figsize=[.5 * 6.4, .5 * 4.8])
plt.scatter(x, y, s=20, color='k')
plt.plot(t, model.predict(t.reshape(-1, 1)), color='C3',
         label='$\hat{f}$')

plt.plot(t, f(t), 'k--', label='$f^{\star}$')
style_figs.no_axis()
plt.legend(loc='upper center', borderaxespad=0, borderpad=0,
           labelspacing=.2, fontsize=26)
plt.subplots_adjust(top=.96)

plt.savefig('polynomial_overfit_simple.svg', facecolor='none', edgecolor='none')

# %%
# A figure with the true model and the estimated one

plt.figure(figsize=[.5 * 6.4, .5 * 4.8])
plt.scatter(x, y, s=20, color='k')
plt.plot(t, model.predict(t.reshape(-1, 1)), color='C3',
         label='$\hat{f}$')

plt.plot(t, f(t), 'k--', label='$f^{\star}$')
style_figs.no_axis()
plt.legend(loc='upper center', borderaxespad=0, borderpad=0,
           labelspacing=.2, fontsize=26)
plt.subplots_adjust(top=.96)


# More detailed legend
plt.savefig('polynomial_overfit_simple_legend.svg', facecolor='none', edgecolor='none')

# %%
# Assymptotic settings

rng = np.random.RandomState(0)
x = 2 * rng.rand(10 * N_SAMPLES) - 1

y = f(x) + .4 * rng.normal(size=10 * N_SAMPLES)


model = make_pipeline(PolynomialFeatures(degree=1), LinearRegression())
model.fit(x.reshape(-1, 1), y)

plt.figure(figsize=[.5 * 6.4, .5 * 4.8])
plt.scatter(x, y, s=20, color='k', alpha=.3)
plt.plot(t, model.predict(t.reshape(-1, 1)), color='C0',
         label='$\hat{f} \\approx f^{\star}$')

plt.plot(t, f(t), 'k--', label='$g$')
style_figs.no_axis()
plt.legend(loc='upper center', borderaxespad=0, borderpad=0,
           labelspacing=.2, fontsize=26)
plt.subplots_adjust(top=.96)

plt.savefig('polynomial_overfit_assymptotic.svg', facecolor='none', edgecolor='none')

# %%
# Validation curves
from sklearn import model_selection
plt.figure()

param_range = np.arange(1, 20)

train_scores, test_scores = model_selection.validation_curve(
    model, x[::2].reshape((-1, 1)), y[::2],
    param_name='polynomialfeatures__degree',
    param_range=param_range,
    cv=model_selection.ShuffleSplit(n_splits=20))

plt.plot(param_range, -np.mean(test_scores, axis=1), 'k',
         label='Generalization error')
plt.plot(param_range, -np.mean(train_scores, axis=1), 'k--',
         label='Training error')

ax = plt.gca()
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)

plt.ylim(ymax=.05)

plt.legend(loc='center')

plt.yticks(())
plt.ylabel('Error')
plt.xlabel('Polynomial degree')
plt.subplots_adjust(left=.07, bottom=.18, top=.99, right=.99)

plt.savefig('polynomial_validation_curve.svg', facecolor='none',
            edgecolor='none')

# %%
# Learning curves
rng = np.random.RandomState(0)
x = 2 * rng.rand(100 * N_SAMPLES) - 1

y = f(x) + .4 * rng.normal(size=100 * N_SAMPLES)

X = x.reshape((-1, 1))

np.random.seed(42)

plt.figure()

def savefig(name):
    " Ajust layout, and then save"
    ax = plt.gca()
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    plt.ylim(-.65, .15)
    plt.xlim(train_sizes.min(), train_sizes.max())
    plt.xticks((100, 1000), ('100', '1000'), size=13)
    plt.yticks(())

    plt.ylabel('Error')
    plt.xlabel('Number of samples')
    plt.subplots_adjust(left=.07, bottom=.16, top=.99, right=.99)
    plt.savefig(name, edgecolor='none', facecolor='none')


# Degree 9
model = make_pipeline(PolynomialFeatures(degree=9), LinearRegression())
train_sizes, train_scores, test_scores = model_selection.learning_curve(
    model, X, y, cv=model_selection.ShuffleSplit(n_splits=20),
    train_sizes=np.logspace(-2.5, -.3, 30))
test_plot = plt.semilogx(train_sizes, -np.mean(test_scores, axis=1),
                            label='9',
                            color='C3')
savefig('polynomial_learning_curve_0.svg')
train_plot = plt.semilogx(train_sizes, -np.mean(train_scores, axis=1), '--',
                            color='C3')

leg1 = plt.legend(['Generalization error', 'Training error'],
                    loc='upper right', borderaxespad=-.2)
savefig('polynomial_learning_curve_1.svg')

# Degree 1
model = make_pipeline(PolynomialFeatures(degree=1), LinearRegression())
train_sizes, train_scores, test_scores = model_selection.learning_curve(
    model, X, y, cv=model_selection.ShuffleSplit(n_splits=20),
    train_sizes=np.logspace(-2.5, -.3, 30))
test_plot = plt.semilogx(train_sizes, -np.mean(test_scores, axis=1),
                            label='1',
                            color='C0')
train_plot = plt.semilogx(train_sizes, -np.mean(train_scores, axis=1), '--',
                            color='C0')


plt.legend(loc='right',
           title='Degree of polynomial', ncol=2)
plt.gca().add_artist(leg1)
savefig('polynomial_learning_curve.svg')

