
package lambda;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;
import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.text.SimpleDateFormat;
//import java.sql.SimpleDateFormat;
import java.util.HashMap;
import java.util.Properties;
import java.util.Scanner;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.S3Object;

import saaf.Response;
import saaf.Inspector;

// your class needs to implement RequestHandler interface to be a Lambda function
public class LoadCSV implements RequestHandler<Request, HashMap<String, Object>> {

	static String CONTAINER_ID = "/tmp/container-id";
	static Charset CHARSET = Charset.forName("US-ASCII");

	public HashMap<String, Object> handleRequest(Request request, Context context) {

		// Collect initial data.
		Inspector inspector = new Inspector();
		// inspector.inspectAll();
		LambdaLogger logger = context.getLogger();

		// ****************START FUNCTION IMPLEMENTATION*************************

		String bucketname = request.getBucketname();
		String filename = request.getFilename();

//		System.out.println("Step1");
//		System.out.println(bucketname);
//		System.out.println(filename);
		String sql = " INSERT INTO SALES_RECORD VALUES(?,?,?,?,?,?,?) ";
		S3Object s3Object = null;

		try {
			// ******************get database connection******************************

			Properties properties = new Properties();
			properties.load(new FileInputStream("db.properties"));
			String url = properties.getProperty("url");
			String username = properties.getProperty("username");
			String password = properties.getProperty("password");
			String driver = properties.getProperty("driver");
//			System.out.println("Step2");
			Connection con = DriverManager.getConnection(url, username, password);
//			System.out.println("Step3");
			PreparedStatement ps = con.prepareStatement("show tables where Tables_in_Testdb='SALES_RECORD'");
			ResultSet rs = ps.executeQuery();
			if (!rs.next()) {
				// table does not exist, and should be created
				logger.log("trying to create table");

				ps = con.prepareStatement(
						"CREATE TABLE SALES_RECORD (Region VARCHAR(255),Country VARCHAR(255),Item_Type VARCHAR(255),Order_Date DATE,OrderPriority CHAR(1),OrderID INT NOT NULL,ShipDate DATE,PRIMARY KEY(OrderID));");
				ps.execute();
//				System.out.println("XYZ");
				// rs.close();
//				System.out.println("lop");
			}
			rs.close();
//			System.out.println("Step4");
//			System.out.println(bucketname);
//			System.out.println(filename);
			// ****************Get S3object to read CSV
			// file******************************************
			AmazonS3 s3Client = AmazonS3ClientBuilder.standard().build();

			s3Object = s3Client.getObject(new GetObjectRequest(bucketname, filename)); // get object file using
			InputStream objectData = s3Object.getObjectContent(); // get content of the file

			// InputStream objectData = s3Object.getObjectContent(); // get content of the
			// file
			String line = "";
			Scanner scanner = new Scanner(objectData); // scanning data line by line

			while (scanner.hasNext()) {
				line = scanner.nextLine();
				if (line.contains("Region,Country,Item Type,Order Priority,Order Date,Order ID,Ship Date")) {
					// Region,Country,Item_Type,Order_Date,OrderPriority,OrderID,ShipDate DATE;
					System.out.println("Continuing for first line.. ");
					continue;
				}
//				System.out.println("Step6");
				if (line != null) {
					String[] array = line.split(",");
					System.out.println(line);
					for (int i = 0; i < array.length; i++) {
						System.out.print(array[i] + " # ");
					}

//					for (String result : array) {
//						System.out.println(result);
//						System.out.println("Step7");
					ps = con.prepareStatement(sql);
					// Australia and Oceania,Tuvalu,Baby Food,H,5/28/2010,669165933,6/27/2010
					SimpleDateFormat formatter = new SimpleDateFormat("mm/dd/yyyy");
					ps.setString(1, array[0]);
					ps.setString(2, array[1]);
					ps.setString(3, array[2]);
					ps.setString(5, array[3]);
//					System.out.println(array[4]);
					ps.setDate(4, new java.sql.Date(formatter.parse(validateDate(array[4])).getTime()));
					ps.setInt(6, Integer.parseInt(array[5]));
//					System.out.println(array[6]);
					ps.setDate(7, new java.sql.Date(formatter.parse(validateDate(array[6])).getTime()));
					ps.executeUpdate();
					ps.close();
//					}
				}
			}
//			System.out.println("Step8");
			scanner.close();

			/*
			 * String loadQuery = "LOAD DATA FROM S3 '" +
			 * "s3://test-bucket1-surbhi/100SalesRecords.csv" +
			 * "' INTO TABLE SALES_RECORD FIELDS TERMINATED BY ','" +
			 * " LINES TERMINATED BY '\n' "; System.out.println(loadQuery);
			 * System.out.println("Step5"); Statement stmt = con.createStatement();
			 * stmt.execute(loadQuery);
			 */
			con.close();

		} catch (Exception e) {
			/// logger.log("Got an exception working with MySQL! ");
			logger.log(e.getMessage());
			e.printStackTrace();
		} finally {
			if (s3Object != null) {
				try {
					s3Object.close();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
		}
		saaf.Response r = new saaf.Response();
		
		System.out.println(bucketname);
		r.setValue("Bucket:" + bucketname + " filename:" + filename);
		System.out.println(filename);
		//r.setNames(filename);
		inspector.consumeResponse(r);
		inspector.inspectAllDeltas();
		return inspector.finish();
	}

	private String validateDate(String date) {
		String[] mm = date.split("/");
		if (mm[0].length() == 1)
			return "0" + date;
		else
			return date;
	}
}
