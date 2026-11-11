// Person segmentation with Apple Vision (runs locally). Usage: swift segment.swift in.jpg out-mask.png
import Foundation
import Vision
import CoreImage
import AppKit

let args = CommandLine.arguments
let inURL = URL(fileURLWithPath: args[1])
let outURL = URL(fileURLWithPath: args[2])
guard let ci = CIImage(contentsOf: inURL) else { fatalError("cannot read image") }

let req = VNGeneratePersonSegmentationRequest()
req.qualityLevel = .accurate
req.outputPixelFormat = kCVPixelFormatType_OneComponent8
let handler = VNImageRequestHandler(ciImage: ci, options: [:])
try handler.perform([req])
guard let buf = req.results?.first?.pixelBuffer else { fatalError("no mask") }

var mask = CIImage(cvPixelBuffer: buf)
// scale mask to the photo size
let sx = ci.extent.width / mask.extent.width, sy = ci.extent.height / mask.extent.height
mask = mask.transformed(by: CGAffineTransform(scaleX: sx, y: sy))
let ctx = CIContext()
guard let cg = ctx.createCGImage(mask, from: ci.extent) else { fatalError("render") }
let rep = NSBitmapImageRep(cgImage: cg)
try rep.representation(using: .png, properties: [:])!.write(to: outURL)
print("ok", Int(ci.extent.width), Int(ci.extent.height))
