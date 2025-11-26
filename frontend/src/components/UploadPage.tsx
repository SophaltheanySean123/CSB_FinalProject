import { useState } from 'react';
import { Upload, FileText, CheckCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';

interface UploadPageProps {
  onUploadComplete: (file: File, questionCount: number) => void;
}

export function UploadPage({ onUploadComplete }: UploadPageProps) {
  const [file, setFile] = useState<File | null>(null);
  const [questionCount, setQuestionCount] = useState<number>(10);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      const fileExtension = selectedFile.name.split('.').pop()?.toLowerCase();
      if (fileExtension === 'pdf' || fileExtension === 'docx' || fileExtension === 'doc' || fileExtension === 'txt') {
        setFile(selectedFile);
      } else {
        alert('Please upload a PDF, Word document, or text file (.pdf, .doc, .docx, .txt)');
      }
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      const fileExtension = droppedFile.name.split('.').pop()?.toLowerCase();
      if (fileExtension === 'pdf' || fileExtension === 'docx' || fileExtension === 'doc' || fileExtension === 'txt') {
        setFile(droppedFile);
      } else {
        alert('Please upload a PDF, Word document, or text file (.pdf, .doc, .docx, .txt)');
      }
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleGenerate = () => {
    if (file) {
      onUploadComplete(file, questionCount);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl mb-4 text-gray-900">AI Quiz Generator</h1>
          <p className="text-gray-600">Upload your study materials and generate customized quizzes instantly</p>
        </div>

        <Card className="p-8 shadow-lg">
          <div className="space-y-6">
            {/* File Upload Area */}
            <div>
              <Label className="text-lg mb-4 block">Upload Document</Label>
              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
                  isDragging
                    ? 'border-indigo-500 bg-indigo-50'
                    : file
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-300 hover:border-indigo-400'
                }`}
              >
                {file ? (
                  <div className="flex items-center justify-center gap-3">
                    <CheckCircle className="w-8 h-8 text-green-600" />
                    <div className="text-left">
                      <p className="text-gray-900">{file.name}</p>
                      <p className="text-gray-500 text-sm">{(file.size / 1024).toFixed(2)} KB</p>
                    </div>
                  </div>
                ) : (
                  <div>
                    <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                    <p className="text-gray-700 mb-2">Drag and drop your file here, or click to browse</p>
                    <p className="text-gray-500 text-sm">Supported formats: PDF, DOC, DOCX, TXT</p>
                  </div>
                )}
                <input
                  type="file"
                  accept=".pdf,.doc,.docx,.txt"
                  onChange={handleFileChange}
                  className="hidden"
                  id="file-upload"
                />
              </div>
              <div className="mt-4 text-center">
                <label htmlFor="file-upload">
                  <Button variant="outline" className="cursor-pointer" asChild>
                    <span>
                      <FileText className="w-4 h-4 mr-2" />
                      {file ? 'Change File' : 'Browse Files'}
                    </span>
                  </Button>
                </label>
              </div>
            </div>

            {/* Question Count Input */}
            <div>
              <Label htmlFor="question-count" className="text-lg mb-4 block">
                Number of Questions
              </Label>
              <div className="flex items-center gap-4">
                <Input
                  id="question-count"
                  type="number"
                  min="1"
                  max="40"
                  value={questionCount}
                  onChange={(e) => {
                    const value = parseInt(e.target.value);
                    if (value >= 1 && value <= 40) {
                      setQuestionCount(value);
                    }
                  }}
                  className="max-w-xs"
                />
                <span className="text-gray-600 text-sm">Maximum: 40 questions</span>
              </div>
              <input
                type="range"
                min="1"
                max="40"
                value={questionCount}
                onChange={(e) => setQuestionCount(parseInt(e.target.value))}
                className="w-full mt-4"
              />
            </div>

            {/* Generate Button */}
            <Button
              onClick={handleGenerate}
              disabled={!file}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-6"
            >
              Generate Quiz ({questionCount} questions)
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
}
