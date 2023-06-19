package mulan.data.characterizer;

import mulan.data.MultiLabelInstances;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by IntelliJ IDEA.
 * User: lenat
 * Date: 22/02/2011
 */
public class Characterizer {

    private List<Characteristic> characteristics;

    public Characterizer(){
        characteristics = new ArrayList<Characteristic>();
    }

    public void addMeasures(Class characteristicsClass) {
        Class<Characteristic>[] stat = (Class<Characteristic>[]) characteristicsClass.getClasses();
        for (Class<Characteristic> aClass : stat) {
            try {
                characteristics.add(aClass.newInstance());
            } catch (InstantiationException e) {
                e.printStackTrace();
            } catch (IllegalAccessException e) {
                e.printStackTrace(); 
            }
        }
    }

    /**
     * Creates a new Characterizer object by deep copying the Characteristic objects that
     * are given as parameters
     *
     * @param someCharacteristics calculated characteristics
     * @throws Exception
     */
    public Characterizer(List<Characteristic> someCharacteristics) throws Exception {
        characteristics = new ArrayList<Characteristic>();
        for (Characteristic m : someCharacteristics) {
            Characteristic newCharacteristic = m.makeCopy();
            characteristics.add(newCharacteristic);
        }
    }

    public String namesToCSV() {
        StringBuilder sb = new StringBuilder();
        for (Characteristic m : characteristics) {
            sb.append(m.getName()).append(';');
        }
        return sb.toString();
    }


    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Results Summary: ").append("\n");
        for (Characteristic m : characteristics) {
            sb.append(m.getName()).append("=").
                    append(m.getValue()).append("\n");
        }
        return sb.toString();
    }

    /**
     * Returns a CSV representation of the calculated measures
     *
     * @return the CSV representation of the calculated measures
     */
    public String toCSV() {
        StringBuilder sb = new StringBuilder();
        for (Characteristic m : characteristics) {
            double value = Double.NaN;
            try {
                value = m.getValue();
            } catch (Exception ex) {
            }
            sb.append(String.format(m.getCSVformat(), value));
            sb.append(";");
        }
        return sb.toString();
    }

    /**
     * Returns the characteristics
     *
     * @return the characteristics
     */
    public List<Characteristic> getCharacteristics() {
        return characteristics;
    }

    public void calculate(MultiLabelInstances train, MultiLabelInstances test) {
        for (Characteristic m : characteristics) {
            m.compute(train,test);
        }
    }

}
