export class FilesMapper {
  static map(file) {
    const { id, fileUrl } = file;
    return {
      id,
      file_url: `http://localhost:5001/${fileUrl}`, // Assuming file_url is the full filename
    };
  }
}
