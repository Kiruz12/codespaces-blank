import java.nio.file.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class F{
    public void read(String filename){
Path ruta = Paths.get(filename);
try (BufferedReader br = Files.newBufferedReader(ruta, StandardCharsets.UTF_8)) {
    String linea;
    while ((linea = br.readLine()) != null) {
        System.out.println(linea);
    }
} catch (IOException e) {
    e.printStackTrace();
}
}
public void write(String filename){
    try{
  Path out = Paths.get(filename) ;
  try (BufferedWriter bw = Files.newBufferedWriter(
          out, StandardCharsets.UTF_8,
          StandardOpenOption.CREATE,
          StandardOpenOption.TRUNCATE_EXISTING)) {
      bw.write("Encabezado\n");
      bw.write("línea 1\n");
  }
}catch(IOException e){
  System.err.println("No se pudo obtener el archivo");
}
}
public static void main(String[]args){
    F f = new F();
    f.read("datos.txt");
    f.write("datos.txt");
}
}
