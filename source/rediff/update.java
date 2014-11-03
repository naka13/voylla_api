import java.io.File;
import java.net.URL;
import java.net.URLClassLoader;
import java.io.IOException;
import rediff.inecom.catalog.product.CSVAPI;

class UpdateClass{
    private final static String api_key = "MTk0Mzctdm95bGxhfENDMTFEODhGOEYzODRFMDEzQkQ4M0I4MkM4NUFDOUE0fDE3ODQ5LXZveWxs YQ==";
    private final static String path = "/home/nish/repos/new/voylla_website/voylla_scripts/rediff/rediff.csv";

    public void updateFunction() {
        CSVAPI cvsapi = new CSVAPI();
        System.out.println(cvsapi);
        try {
            String output = cvsapi.UpdateCSVAPI(api_key,path);
            System.out.println(output);
            System.out.println("Success!");
        }
        catch (Exception e) {
            System.out.println("catch");
            e.printStackTrace(); 
        }
    }

    public static void main(String args[]){
        new UpdateClass().updateFunction();
    }
}
