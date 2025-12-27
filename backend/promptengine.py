def buildprompt(condition,gender,bodytype,pattern_name='none'):
    match gender.lower():
        case 'male':
            
            model_desc=("a professional male fashion model with sharp features, "
                        "natural skin texture, and a confident editorial pose")
        case _:
            model_desc=("a professional female fashion model with elegant posture, "
                        "natural skin texture, and a sophisticated editorial look")
        
    match bodytype:
        case 'Full-Body':
            
            framing_desc=("a full-body standing shot, head-to-toe view, 85mm lens, "
                          "captured in a high-end fashion studio with a clean cyclorama background")
        case "Upper-Body":
            
             framing_desc=("a medium waist-up portrait, focusing on the torso and arms, "
                           "macro-detail on fabric, shallow depth of field with soft bokeh")
        case _:
            
             framing_desc = ("a lower-body shot from the navel to the floor, focusing on leg posture "
                             "and footwear, sharp focus on fabric folds and leg silhouette")
    
    
    base=(f"professional fashion photography of{model_desc}"
          f"the image must be of {framing_desc},studio lighting,highly realistic")
    
    match condition:
        case "simple try on":
            
            return base+("The model must be wearing the exact clothing item from the uploaded photo. "
                         "Preserve the original colors, patterns, and fabric texture perfectly."
                         "Ensure the clothing fits naturally on the model's body.")
        case _:
            
            return base +(f"Take the structural shape of the uploaded clothing, "
                         f"but apply a high-quality {pattern_name} print texture to it. "
                         "The final result should look like a real, manufactured garment." )
    
   