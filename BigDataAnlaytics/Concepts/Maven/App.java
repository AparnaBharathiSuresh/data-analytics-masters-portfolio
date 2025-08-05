package edu.sjsu.data228.aparnasuresh;
import java.time.LocalDate;
import java.util.Random;

/**
 * Hello world!
 */
public class App {
    public static void main(String[] args) {
        System.out.println("Hello World, Aparna");
		LocalDate date = LocalDate.now();
		System.out.println("Today is "+date);
		Random num = new Random();
		int n= num.nextInt(50);
		System.out.println("Random Number is " +n);
		int squaren=n*n;
		System.out.println("Square of " +n+ " is " +squaren);
    }
}
