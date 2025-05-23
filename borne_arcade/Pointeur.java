import java.io.IOException;

import MG2D.geometrie.Texture;
import MG2D.geometrie.Couleur;
import MG2D.geometrie.Point;
import MG2D.geometrie.Triangle;
import MG2D.Clavier;


public class Pointeur {
    private int value;
    private Texture triangleGauche;
    private Texture triangleDroite;
    private Texture rectangleCentre;

    public Pointeur(){
	this.triangleGauche = new Texture("img/star.png", new Point(30, 492), 40,40);
	// this.triangleDroite = new Triangle(Couleur .ROUGE, new Point(550, 560), new Point(520, 510), new Point(550, 460), true);
	this.triangleDroite = new Texture("img/star.png", new Point(530, 492), 40,40);
	this.rectangleCentre = new Texture("img/select2.png", new Point(80, 460), 440, 100);
	this.value = Graphique.tableau.length-1;
    }

    public void lancerJeu(ClavierBorneArcade clavier){
	if(clavier.getBoutonJ1ATape()){

	    //System.out.println(Graphique.tableau[getValue()].getChemin());
	    try {
		Graphique.stopMusiqueFond();
		Process process = Runtime.getRuntime().exec("./"+Graphique.tableau[getValue()].getNom()+".sh");
		process.waitFor();		//ajouté afin d'attendre la fin de l'exécution du jeu pour reprendre le contrôle sur le menu
		Graphique.lectureMusiqueFond();
	    } catch (IOException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	    } catch(Exception e){	//on catche toutes les exceptions, nécessaire pour le waitFor()
			e.printStackTrace();
		}

	    //System.out.println("le process sur "+Graphique.tableau[getValue()].getChemin()+" est bien lancé");
	}
    }

    public int getValue() {
	return value;
    }

    public void setValue(int value) {
	this.value = value;
    }

    public Texture getTriangleGauche() {
	return triangleGauche;
    }

    public void setTriangleGauche(Texture triangleGauche) {
	this.triangleGauche = triangleGauche;
    }

    public Texture getTriangleDroite() {
	return triangleDroite;
    }

    public void setTriangleDroite(Texture triangleDroite) {
	this.triangleDroite = triangleDroite;
    }

    public Texture getRectangleCentre() {
	return rectangleCentre;
    }

    public void setRectangleCentre(Texture rectangleCentre) {
	this.rectangleCentre = rectangleCentre;
    }

}
