import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.io.LongWritable;



import java.io.IOException;

public class LongestWordMapper extends Mapper<LongWritable, Text, IntWritable, Text> {

    private final static IntWritable wordLength = new IntWritable();
    private final Text word = new Text();

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String[] words = value.toString().split("\\W+"); // Split on non-word characters

        for (String w : words) {
            if (!w.isEmpty()) {
                word.set(w);
                wordLength.set(w.length());
                context.write(wordLength, word); 
            }
        }
			
    }
}
