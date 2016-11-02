import java.util.Scanner;

public class Factorial{
    public static int fact(int n){
        if(n == 0 || n == 1){
            return 1;
        }
        return n * fact(n-1);
    }
    public static void main(String[] args){
        Scanner reader = new Scanner(System.in);
        int n = reader.nextInt();
        int f = Factorial.fact(n);
        System.out.println(f);
    }
}
