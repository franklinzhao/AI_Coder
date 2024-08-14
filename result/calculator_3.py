#```java
import java.util.InputMismatchException;
import java.util.Scanner;
import java.util.logging.Logger;

public class Calculator {

    private static final Logger logger = Logger.getLogger(Calculator.class.getName());

    public static void main(String[] args) {
        try {
            Scanner scanner = new Scanner(System.in);
            System.out.println("Simple Calculator");
            System.out.println("1. Addition");
            System.out.println("2. Subtraction");
            System.out.println("3. Multiplication");
            System.out.println("4. Division");
            System.out.println("5. Exponentiation");
            System.out.println("6. Logarithm");

            System.out.print("Choose an operation (1-6): ");
            int choice = scanner.nextInt();

            System.out.print("Enter first number: ");
            double num1 = scanner.nextDouble();

            System.out.print("Enter second number: ");
            double num2 = scanner.nextDouble();

            switch (choice) {
                case 1:
                    System.out.println("Result: " + add(num1, num2));
                    break;
                case 2:
                    System.out.println("Result: " + subtract(num1, num2));
                    break;
                case 3:
                    System.out.println("Result: " + multiply(num1, num2));
                    break;
                case 4:
                    System.out.println("Result: " + divide(num1, num2));
                    break;
                case 5:
                    System.out.println("Result: " + exponentiate(num1, num2));
                    break;
                case 6:
                    System.out.println("Result: " + logarithm(num1, num2));
                    break;
                default:
                    System.out.println("Invalid choice");
            }
        } catch (InputMismatchException e) {
            logger.severe("Invalid input. Please enter a number.");
        } catch (ArithmeticException e) {
            logger.severe("Arithmetic error: " + e.getMessage());
        } catch (Exception e) {
            logger.severe("An error occurred: " + e.getMessage());
        }
    }

    public static double add(double num1, double num2) {
        return num1 + num2;
    }

    public static double subtract(double num1, double num2) {
        return num1 - num2;
    }

    public static double multiply(double num1, double num2) {
        return num1 * num2;
    }

    public static double divide(double num1, double num2) {
        if (num2 == 0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        return num1 / num2;
    }

    public static double exponentiate(double num1, double num2) {
        return Math.pow(num1, num2);
    }

    public static double logarithm(double num1, double num2) {
        if (num1 <= 0 || num2 <= 0) {
            throw new ArithmeticException("Cannot calculate logarithm of non-positive number");
        }
        return Math.log(num1) / Math.log(num2);
    }
}
#```