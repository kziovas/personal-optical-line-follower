class PID:
    """
    PID controller Class for precise movement
    e.x. mot_pid = PID(P parameter,I parameter,K parameter)
    """

    def __init__(self, KP=0, KI=0, KD=0):
        self.error_prior = 0
        self.integral = 0
        self.KP = KP
        self.KI = KI
        self.KD = KD

    def calculate_response(self, desired_value, actual_value, start_time, end_time):
        error = desired_value - actual_value
        iteration_time = end_time - start_time
        self.integral = self.integral + (error * iteration_time)
        derivative = (error - self.error_prior) / iteration_time
        output = self.KP * error + self.KI * self.integral + self.KD * derivative
        self.error_prior = error
        return output

    def reset_error(self):
        self.error_prior = 0
        self.integral = 0

    def update_parameters(self, KP, KI, KD):
        self.KP = KP
        self.KI = KI
        self.KD = KD
        self.error_prior = 0
        self.integral = 0
