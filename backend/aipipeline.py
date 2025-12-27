import google.generativeai as genai
import concurrent.futures
from .promptengine import buildprompt
from .imagelogic import prepareimage
def run_singlegeneration(shirtfile, gender, bodytype, patternfile=None):
    try:
        api_key="GEMINIAPI_KEY"
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') 
        processed_shirt = prepareimage(shirtfile)
        
      
        if patternfile:
         
            processed_pattern = prepareimage(patternfile)
            prompt_text = buildprompt('texture overlay', gender, bodytype)
            content_list = [prompt_text, processed_shirt, processed_pattern]
        else:
           
            prompt_text = buildprompt('virtual try on', gender, bodytype)
            content_list = [prompt_text, processed_shirt]
            
    
        response = model.generate_content(content_list)
        
        if response.images:
            return response.images[0]
        else:
            return "ERROR: AI failed to generate image."
            
    except Exception as e:
        return f"error: {str(e)}"

def runbatch_pipeline(uploade_files, gender, bodytype, pattern_file=None):
    all_result = []
   
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future_to_file = {
            executor.submit(run_singlegeneration, file, gender, bodytype, pattern_file): file
            for file in uploade_files
        }
        
        for future in concurrent.futures.as_completed(future_to_file):
            file_name = future_to_file[future].name
            try:
                output_image = future.result()
                all_result.append({
                    "file_name": file_name,
                    "output": output_image
                })
            except Exception as e:
                all_result.append({
                    "file_name": file_name, 
                    "output": f"Failed: {str(e)}"
                })
                
    return all_result