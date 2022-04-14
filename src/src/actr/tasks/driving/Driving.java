package actr.tasks.driving;

import java.awt.*;
import java.util.*;
import java.util.List;
import javax.swing.*;

import actr.task.*;

/**
 * The main Driving task class that sets up the simulation and starts periodic updates.
 *  
 * @author Dario Salvucci
 */
public class Driving extends actr.task.Task
{
	static Simulator simulator = null;

	Simulation simulation;
	JLabel nearLabel, carLabel, keypad;

	final double scale = .6; // .85
	final double steerFactor_dfa = (16 * scale);
	final double steerFactor_dna = (4 * scale);
	final double steerFactor_na  = (3 * scale);
	final double steerFactor_fa  = (0 * scale);
	final double accelFactor_thw  = (1 * .40);
	final double accelFactor_dthw = (3 * .40);
	final double steerNaMax = .07;
	final double thwFollow = 1.0;
	final double thwMax = 4.0;

	double startTime=0, endTime=60;
	double accelBrake=0, speed=0;

	static int minX=174, maxX=(238+24), minY=94, maxY=(262+32);
	static int centerX=(minX+maxX)/2, centerY=(minY+maxY)/2;

	List<String> output = new ArrayList<String>();

	public Driving ()
	{
		super ();
		nearLabel = new JLabel (".");
		carLabel = new JLabel ("X");
		keypad = new JLabel ("*");
	}

	public void start ()
	{
		simulation = new Simulation (getModel());

		if (getModel().getRealTime())
		{
			setLayout (new BorderLayout());
			if (simulator == null) simulator = new Simulator ();
			add (simulator, BorderLayout.CENTER);
			simulator.useSimulation (simulation);
		}
		else
		{
			add (nearLabel);
			nearLabel.setSize (20, 20);
			nearLabel.setLocation (250, 250);
			add (carLabel);
			carLabel.setSize (20, 20);
			carLabel.setLocation (250, 250);
			add (keypad);
			keypad.setSize (20, 20);
			int keypadX = 250 + (int) (actr.model.Utilities.angle2pixels (10.0));
			keypad.setLocation (keypadX, 250);
		}

		getModel().runCommand ("(set-visual-frequency near .1)");
		getModel().runCommand ("(set-visual-frequency car .1)");

		accelBrake = 0;
		speed = 0;

		getModel().getVision().addVisual ("near", "near", "near", nearLabel.getX(), nearLabel.getY(), 1, 1, 10);
		getModel().getVision().addVisual ("car", "car", "car", carLabel.getX(), carLabel.getY(), 1, 1, 100);
		getModel().getVision().addVisual ("keypad", "keypad", "keypad", keypad.getX(), keypad.getY(), 1, 1);

		addPeriodicUpdate (Env.sampleTime);
	}

	public void update (double time)
	{
		if (time <= endTime)
		{
			simulation.env.time = time - startTime;
			simulation.update();
			updateVisuals();
		}
		else {
			String filename = "_behavior_";
			if (simulation.model.behaviorOut) {
				List<String> output = output(simulation.samples);
				simulation.model.print(output, filename);
			}
			getModel().stop();
		}
	}

	List<String> output(Vector<Sample> samples) {
		for (int i = 1; i < samples.size(); i++) {
			Sample s = samples.elementAt(i);
			if (i == 1) {
				output.add(s.listVarsSep() + System.lineSeparator());
				output.add(s.toStringSep() + System.lineSeparator());
			} else
				output.add(s.toStringSep() + System.lineSeparator());
		}
		return output;
		// Model.print(output, "_driving_");
	}

	void updateVisuals ()
	{
		Env env = simulation.env;
		if (env.simcar.nearPoint != null)
		{
			Coordinate cn = env.world2image (env.simcar.nearPoint);
			Coordinate cc = env.world2image (env.simcar.carPoint);
			//Coordinate cc = env.world2image (env.simcar.farPoint);

			if (cn == null || cc == null) env.done = true;
			else
			{
				nearLabel.setLocation (cn.x, cn.y);
				carLabel.setLocation (cc.x, cc.y);
				getModel().getVision().moveVisual ("near", cn.x, cn.y);
				getModel().getVision().moveVisual ("car", cc.x, cc.y);
//				getModel().getVision().moveVisual ("near", cn.x+5, cn.y+10);
//				getModel().getVision().moveVisual ("car", cc.x+5, cc.y+10);
				speed = env.simcar.speed;
			}
		}
	}

	double minSigned (double x, double y)
	{
		return (x>=0) ? Math.min (x,y) : Math.max (x,-y);
	}

	void doSteer (double na, double dna, double dfa, double dt)
	{
		Simcar simcar = simulation.env.simcar;
		if (simcar.speed >= 10.0)
		{
			double dsteer = (dna * steerFactor_dna)
			+ (dfa * steerFactor_dfa)
			+ (minSigned (na, steerNaMax) * steerFactor_na * dt);
			dsteer *= simulation.driver.steeringFactor;
			simcar.steerAngle += dsteer;
		}
		else simcar.steerAngle = 0;
	}

	void doAccelerate (double fthw, double dthw, double dt)
	{
		Simcar simcar = simulation.env.simcar;
		if (simcar.speed >= 10.0)
		{
			double dacc = (dthw * accelFactor_dthw)
			+ (dt * (fthw - thwFollow) * accelFactor_thw);
			accelBrake += dacc;
			accelBrake = minSigned (accelBrake, 1.0);
		}
		else
		{
			accelBrake = .65 * (simulation.env.time / 3.0);
			accelBrake = minSigned (accelBrake, .65);
		}
		simcar.accelerator = (accelBrake >= 0) ? accelBrake : 0;
		simcar.brake = (accelBrake < 0) ? -accelBrake : 0;
	}

	boolean isCarStable (double na, double nva, double fva)
	{
		double f = 2.5;
		return (Math.abs(na) < .025*f) && (Math.abs(nva) < .0125*f) && (Math.abs(fva) < .0125*f);
	}

	double image2angle (double x, double d)
	{
		Env env = simulation.env;
		double px = env.simcar.p.x + (env.simcar.h.x * d);
		double pz = env.simcar.p.z + (env.simcar.h.z * d);
		Coordinate im = env.world2image (new Position (px, pz));
		try { return Math.atan2 (.5*(x-im.x), 450); }
		catch (Exception e) { return 0; }
	}

	public void eval (Iterator<String> it)
	{
		it.next(); // (
		String cmd = it.next();
		if (cmd.equals ("do-steer"))
		{
			double na = Double.valueOf (it.next());
			double dna = Double.valueOf (it.next());
			double dfa = Double.valueOf (it.next());
			double dt = Double.valueOf (it.next());
			doSteer (na, dna, dfa, dt);
		}
		else if (cmd.equals ("do-accelerate"))
		{
			double fthw = Double.valueOf (it.next());
			double dthw = Double.valueOf (it.next());
			double dt = Double.valueOf (it.next());
			doAccelerate (fthw, dthw, dt);
		}
	}

	public boolean evalCondition (Iterator<String> it)
	{
		it.next(); // (
		String cmd = it.next();
		if (cmd.equals ("is-car-stable") || cmd.equals ("is-car-not-stable"))
		{
			double na = Double.valueOf (it.next());
			double nva = Double.valueOf (it.next());
			double fva = Double.valueOf (it.next());
			boolean b = isCarStable(na,nva,fva);
			return cmd.equals("is-car-stable") ? b : !b;
		}
		else return false;
	}

	public double bind (Iterator<String> it)
	{
		try
		{
			it.next(); // (
			String cmd = it.next();
			if (cmd.equals ("image->angle"))
			{
				double x = Double.valueOf (it.next());
				double d = Double.valueOf (it.next());
				return image2angle (x, d);
			}
			else if (cmd.equals ("mp-time")) return simulation.env.time;
			else if (cmd.equals ("get-thw"))
			{
				double fd = Double.valueOf (it.next());
				double v = Double.valueOf (it.next());
				double thw = (v==0) ? 4.0 : fd/v;
				return Math.min (thw, 4.0);
			}
			else if (cmd.equals ("get-velocity")) return speed;
			else return 0;

		}
		catch (Exception e)
		{
			e.printStackTrace();
			System.exit(1);
			return 0;
		}
	}

	public int numberOfSimulations () { return 1; }

	public Result analyze (Task[] tasks, boolean output)
	{
		return null;
	}
}
