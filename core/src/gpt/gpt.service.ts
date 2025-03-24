import { Injectable } from '@nestjs/common';
import OpenAI from 'openai';
import { env } from 'process';

@Injectable()
export class GptService {
  private openai: OpenAI;

  constructor() {
    this.openai = new OpenAI({
      apiKey: env.OPEN_AI, // Store API key in .env
    });
  }

  async generateFace(data: any) {
    const prompt = this.createPrompt(data);

    const responses = await Promise.all([
      this.generateImage(prompt, 'front'),
      this.generateImage(prompt, 'left'),
      this.generateImage(prompt, 'right'),
    ]);

    return {
      front: responses[0],
      left: responses[1],
      right: responses[2],
    };
  }

  private createPrompt(data: any): string {
    return `A highly detailed and realistic portrait of a ${data.Ethnicity} ${data.Gender} with the following features:
    - Face Shape: ${data.Face_Shape}
    - Eye Color: ${data.Eye_Color}
    - Hair Color: ${data.Hair_Color}
    - Skin Color: ${data.Skin_Color}
    - Nose: ${data.Nose_Shape}, Size: ${data.Nose_Size}
    - Ear Shape: ${data.Ear_Shape}
    - Handedness: ${data.Handedness}
    - Sleep Pattern: ${data.Sleep_Pattern}
    - Body Odor: ${data.Body_Odor} (not visually represented)
    - Reaction Time: ${data.Reaction_Time} (not visually represented)
    - Alcohol Consumption: ${data.Alcohol_Consumption} (not visually represented)
    - ASPD Psychopathy Level: ${data.ASPD_Psychopathy_Level} (neutral facial expression)
    - Depression Level: ${data.Depression_Level} (neutral but slightly subdued expression)
    - Diabetic Level: ${data.Diabetic_Level} (slight skin tone variations to reflect health condition)
    - Heart Disease Rate: ${data.Heart_Disease_Rate} (subtle visual cues if applicable)
    - Sickness: ${data.Sickness} (subtle health-related visual cues)

    Ensure hyper-realism, natural lighting, and high skin texture detail.
    
    Generate three different perspectives:
    1. Front-facing view (Neutral pose, looking directly at the camera)
    2. Left-side view (Head slightly turned left)
    3. Right-side view (Head slightly turned right)

    The subject should be shown from the shoulders up.`;
  }

  private async generateImage(prompt: string, angle: string) {
    const response = await this.openai.images.generate({
      model: 'dall-e-3',
      prompt: `${prompt} Show the face from the ${angle} view.`,
      n: 1,
      size: '1024x1024',
    });

    return response.data[0].url; // Return the generated image URL
  }
}
