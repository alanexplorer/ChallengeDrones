class PIDController:
    def __init__(self, kp, ki, kd):
        """
        Inicializa um controlador PID com os coeficientes especificados.

        Args:
            kp (float): Coeficiente proporcional (P).
            ki (float): Coeficiente integral (I).
            kd (float): Coeficiente derivativo (D).
        """
        self.kp = kp  # Armazena o coeficiente proporcional.
        self.ki = ki  # Armazena o coeficiente integral.
        self.kd = kd  # Armazena o coeficiente derivativo.
        self.prev_error = 0  # Inicializa o erro anterior como zero.
        self.integral = 0  # Inicializa a soma dos erros (integral) como zero.

    def update(self, error):
        """
        Calcula a saída de controle com base no erro atual.

        Args:
            error (float): O erro atual entre o valor desejado e o valor real.

        Returns:
            float: A saída de controle calculada.
        """
        p = self.kp * error  # Termo proporcional (P).

        self.integral += error  # Soma o erro atual à integral acumulada.
        i = self.ki * self.integral  # Termo integral (I).

        d = self.kd * (error - self.prev_error)  # Termo derivativo (D).
        self.prev_error = error  # Atualiza o erro anterior.

        control_output = p + i + d  # Calcula a saída de controle combinada.

        return control_output  # Retorna a saída de controle calculada.

# Exemplo de uso:
# pid = PIDController(kp, ki, kd)  # Crie uma instância do controlador PID com os coeficientes desejados.
# control_output = pid.update(error)  # Calcule a saída de controle com base no erro atual.
