package actr.tasks.driving;

/**
 * A class that defines the particular scenario represented by the driving environment.
 *  
 * @author Dario Salvucci
 */
public class Scenario
{
	boolean curvedRoad = false;
	boolean simCarConstantSpeed = true; // false;
	int simCarMPH = 55;
	boolean leadCarConstantSpeed = true;
	int leadCarMPH = 55;
	boolean leadCarBrakes = true;
	int drivingMinutes = 15;
	int timeBetweenTrials = 240;
	boolean baselineOnly = false;
	
	Scenario () { }

	String writeString ()
	{
		String s = new String ("");
		s += ((curvedRoad) ? 1 : 0) + "\t";
		s += ((simCarConstantSpeed) ? 1 : 0) + "\t";
		s += Integer.toString(simCarMPH) + "\t";
		s += ((leadCarConstantSpeed) ? 1 : 0) + "\t";
		s += Integer.toString(leadCarMPH) + "\t";
		s += ((leadCarBrakes) ? 1 : 0) + "\t";
		s += drivingMinutes + "\t";
		s += timeBetweenTrials;
		return s;
	}
	
//	static Scenario readString (MyStringTokenizer st)
//	{
//		Scenario s = new Scenario();
//		s.curvedRoad = (st.nextInt() == 1);
//		s.simCarConstantSpeed = (st.nextInt() == 1);
//		s.simCarMPH = st.nextInt();
//		s.leadCarConstantSpeed = (st.nextInt() == 1);
//		s.leadCarMPH = st.nextInt();
//		s.leadCarBrakes = (st.nextInt() == 1);		
//		s.drivingMinutes = st.nextInt();
//		s.timeBetweenTrials = st.nextInt();
//		return s;
//	}
}
