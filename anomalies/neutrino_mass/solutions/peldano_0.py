"""Peldano 0 -- dimensional estimate of the neutrino mass scale."""


def m_nu_estimate(y: float, v: float, M: float) -> float:
    """m_nu ~ y^2 v^2 / M -- the natural seesaw-like dimensional estimate.

    Args:
        y: a Yukawa-like dimensionless coupling.
        v: the electroweak scale (GeV).
        M: the heavy scale suppressing the mass (GeV).

    Returns:
        m_nu in the same mass units as v and M.
    """
    return y**2 * v**2 / M
