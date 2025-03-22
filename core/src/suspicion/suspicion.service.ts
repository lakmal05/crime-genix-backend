import { Injectable } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import axios from 'axios';
const STR_MARKERS = ['AGAT', 'TCTA', 'GATA', 'CGTA'];

@Injectable()
export class SuspicionService {
  constructor(private readonly prismaService: PrismaService) {}

  private extractStrCounts(dnaSequence: string): number[] {
    return STR_MARKERS.map((marker) => {
      const regex = new RegExp(`(${marker})+`, 'g');
      const matches = dnaSequence.match(regex) || [];
      return matches.length;
    });
  }
  private countStrRepeats(dnaSequence: string, strMarkers: string[]): number[] {
    return strMarkers.map((marker) => {
      const regex = new RegExp(marker, 'g');
      const matches = dnaSequence.match(regex);
      return matches ? matches.length : 0;
    });
  }

  async create(data: any) {
    const requestBody = {
      dna_sequence: data.dna,
    };
    const response = await axios.post(
      'http://127.0.0.1:5000/predict',
      requestBody,
    );
    console.log(response, 'dnaa');
    const dna_data_object = response.data;
    const strVector = await this.countStrRepeats(data.dna, STR_MARKERS);
    const fileIds = data.fileIds;
    return await this.prismaService.suspicion.create({
      data: {
        name: data.name,
        nic: data.nic,
        description: data.description,
        age: data.age,
        pastCriminalRecords: data.pastCriminalRecords,
        dna: data.dna,
        strVector: JSON.stringify(strVector),
        metaData: dna_data_object,
        gender: data.gender,
        files: {
          connect: fileIds?.map((id) => ({ id })),
        },
      },
    });
  }

  async findAll() {
    const suspicions = await this.prismaService.suspicion.findMany({
      include: {
        files: true,
        createdBy: true,
      },
    });
    return suspicions.map((suspicion) => ({
      ...suspicion,
      files: suspicion.files.map((file) => ({
        ...file,
        fileUrl: `http://localhost:5001/${file.fileUrl}`, // Correctly map the file URL
      })),
    }));
  }

  async findById(id: string) {
    const numericId = parseInt(id, 10);
    const suspicion = await this.prismaService.suspicion.findUnique({
      where: {
        id: numericId,
      },
      include: {
        files: true,
      },
    });

    if (!suspicion) {
      return null; // Handle the case where no suspicion is found
    }

    return {
      ...suspicion,
      files: suspicion.files.map((file) => ({
        ...file,
        fileUrl: `http://localhost:5001/${file.fileUrl}`, // Map the file URL
      })),
    };
  }
  update(data: any) {
    return this.prismaService.suspicion.update({
      where: {
        id: data.id,
      },
      data: {
        name: data.name,
        nic: data.nic,
        description: data.description,
        age: data.age,
        pastCriminalRecords: data.pastCriminalRecords,
        dna: data.dna,
        gender: data.gender,
      },
    });
  }

  delete(suspicionId: string) {
    const numericId = parseInt(suspicionId, 10);
    return this.prismaService.suspicion.delete({
      where: {
        id: numericId,
      },
    });
  }
}

// name: fullName,
// contactNo: contactNo,
// age: age,
// NICNumber: NICNumber,
// description: description,
// pastCriminalRecords: pastCriminalRecords,
// gender: gender,
// perpetratorProfileImgs: perpetratorProfileImgs,
// DNASequence: DNASequence,
