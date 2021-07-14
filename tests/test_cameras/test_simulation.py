"""Test simulated camera."""

from rpyscope.cameras.simulation import SimCam


def test_sim_cam_function_call():
    """Make sure that function call is returned back as string."""
    sim_cam = SimCam()
    ret_sim = sim_cam.test(42)
    ret_exp = "Function: test / Arguments: 42"
    assert ret_sim == ret_exp
