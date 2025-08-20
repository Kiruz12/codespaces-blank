import java.nio.file.*;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class F{
    public void read(){
Path ruta = Paths.get("datos.txt");
try (BufferedReader br = Files.newBufferedReader(ruta, StandardCharsets.UTF_8)) {
    String linea;
    while ((linea = br.readLine()) != null) {
        System.out.println(linea);
    }
} catch (IOException e) {
    e.printStackTrace();
}
}
public static void main(String[]args){
    F f = new F();
    f.read();
}
}
