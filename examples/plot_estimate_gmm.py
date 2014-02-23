import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import check_random_state
from gmr import GMM, plot_error_ellipses


if __name__ == "__main__":
    random_state = check_random_state(0)
    n_samples = 200
    n_features = 2
    X = np.ndarray((n_samples, n_features))
    X[:n_samples / 2, :] = random_state.multivariate_normal(
        [0.0, 1.0], [[0.5, -2.0], [-2.0, 5.0]], size=(n_samples / 2,))
    X[-n_samples / 2:, :] = random_state.multivariate_normal(
        [3.0, 1.0], [[3.0, 2.0], [2.0, 1.0]], size=(n_samples / 2,))

    gmm = GMM(n_components=2, random_state=random_state)
    gmm.from_samples(X)

    cond = gmm.condition(np.array([1]), np.array([[0.5]]))
    plt.figure()
    X_test = np.linspace(-10, 10, 100)
    plt.plot(X_test, cond.to_probability_density(X_test[:, np.newaxis]))

    plt.figure()
    plt.axis("equal")
    plot_error_ellipses(plt.gca(), gmm, colors=["r", "g"])
    plt.scatter(X[:, 0], X[:, 1])
    plt.xlim((-10, 10))
    plt.ylim((-10, 10))

    plt.figure()
    x, y = np.meshgrid(np.linspace(-10, 10, 100), np.linspace(-10, 10, 100))
    X_test = np.vstack((x.ravel(), y.ravel())).T
    p = gmm.to_probability_density(X_test)
    p = p.reshape(*x.shape)
    plt.contourf(x, y, p)
    X_sampled = gmm.sample(100)
    plt.scatter(X_sampled[:, 0], X_sampled[:, 1], c="r")
    plt.show()
